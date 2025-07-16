import os
from dotenv import load_dotenv
import requests
import spacy
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Chat
import bleach

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)


nlp = spacy.load("en_core_web_md")

# Load medical terms for similarity checking
def load_medical_terms(file_path):
    try:
        with open(file_path, 'r') as file:
            return [nlp(line.strip()) for line in file.readlines() if line.strip()]
    except Exception as e:
        logging.error(f"Error loading medical terms: {e}")
        return []

core_terms = load_medical_terms('medical_term.txt')

# Groq API Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# =
GROQ_HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

#prompt for Groq
SYSTEM_PROMPT = (
    "You are a knowledgeable and empathetic medical assistant AI designed to provide helpful information. "
    "Always tailor your response to the user's specific condition or symptoms, using the provided conversation history to maintain context. "
    "Do NOT provide definitive diagnoses, harmful advice, or speculative answers. For unclear inputs, ask clarifying questions or admit uncertainty. "
    "Use plain, layperson-friendly language, explaining medical terms if needed.\n\n"
    "Your output MUST:\n"
    "- Start with a brief empathetic acknowledgement (e.g., 'I'm sorry you're feeling this way'), but make sure its only at the start of a diagnosis,if its a follow-up dont repeat also you don't always have to be sorry just read the situation.\n"
    "- List potential causes related only to the user's input, avoiding unrelated conditions.\n"
    "- Use <ul> and <li> tags for bullet lists.\n"
    "- Use <strong> to highlight symptom names, conditions, or key terms.\n"
    "- Provide actionable, safe, and relevant suggestions, avoiding repetition unless applicable.\n"
    "- For urgent symptoms (e.g., chest pain, difficulty breathing), urge the user to seek immediate medical attention.\n"
    "- Include a disclaimer: 'This information is for general guidance only. Always consult a healthcare professional for personalized advice, diagnosis, or treatment.'\n"
    "- Do NOT include markdown, code formatting, or technical jargon unless explained.\n"
    "- Do NOT provide vague or identical responses for different symptoms.\n"
)

#formatting for medical queries
# def format_medical_response(query):
#     return f"""
#     <p><strong>I'm here to assist you with your health concern:</strong> {query}</p>
    
#     <h3>Possible Causes:</h3>
#     <ul>
#         <li><strong>Tension or stress</strong></li>
#         <li><strong>Dehydration</strong></li>
#         <li><strong>Fatigue or lack of sleep</strong></li>
#         <li><strong>Infections</strong> (e.g., cold, flu)</li>
#         <li><strong>Environmental factors</strong> (e.g., allergens, weather changes)</li>
#         <li><strong>Underlying medical conditions</strong> (e.g., chronic conditions)</li>
#     </ul>
    
#     <h3>Common Symptoms to Look Out For:</h3>
#     <ul>
#         <li>How long have you been experiencing these symptoms?</li>
#         <li>Do you feel any other related symptoms (e.g., fever, nausea, fatigue)?</li>
#     </ul>
    
#     <h3>General Recommendations:</h3>
#     <ul>
#         <li><strong>Rest:</strong> Take a break and relax in a quiet, dark space.</li>
#         <li><strong>Hydrate:</strong> Drink plenty of water or fluids to stay hydrated.</li>
#         <li><strong>Healthy Eating:</strong> Try to eat balanced meals with sufficient nutrients.</li>
#         <li><strong>Relaxation:</strong> Use relaxation techniques like deep breathing or meditation.</li>
#     </ul>
    
#     <p><strong>Disclaimer:</strong> These are general suggestions. Always consult with a healthcare professional for personalized medical advice, diagnosis, or treatment.</p>
    
#     <p>Let me know if you need further assistance or have more specific questions!</p>
#     """
# Template to format conversation history
TEMPLATE = '''
{context}
User: {question}
Note: The user is seeking help for a medical concern. Please analyze the unique condition mentioned and tailor your advice accordingly.
'''


# Call Groq API with prompt
def call_groq_model(prompt):
    try:
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        response = requests.post(GROQ_API_URL, headers=GROQ_HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        if not content:
            logging.warning("Groq API returned empty content.")
            return None  # Trigger fallback
        return content
    except requests.exceptions.HTTPError as e:
        logging.error(f"Groq API HTTP error: {e}, Response: {e.response.text if e.response else 'No response'}")
        if e.response.status_code == 401:
            return None  # Trigger fallback for auth issues
        elif e.response.status_code == 429:
            logging.warning("Groq API rate limit exceeded.")
            return None  # Trigger fallback for rate limits
        return None  # Trigger fallback for other HTTP errors
    except Exception as e:
        logging.error(f"Groq API general error: {e}")
        return None  # Trigger fallback

# Determine if input is medical-related
def is_medical_question(user_input, threshold=0.5):
    if not core_terms:
        logging.warning("Medical terms list is empty.")
        return False
    user_doc = nlp(user_input.lower())
    return any(user_doc.similarity(term_doc) > threshold for term_doc in core_terms)

# Maintain conversation context in database
async def update_context(db: AsyncSession, user_id: int, user_input: str, response: str, max_turns: int = 5):
    result = await db.execute(
        select(Chat).where(Chat.user_id == user_id).order_by(Chat.timestamp.desc()).limit(max_turns)
    )
    chats = result.scalars().all()
    context_lines = []
    for chat in reversed(chats):
        context_lines.append(f"User: {chat.message}")
        context_lines.append(f"AI: {chat.response}")
    context_lines.append(f"User: {user_input}")
    context_lines.append(f"AI: {response}")
    return '\n'.join(context_lines)

# Main chat handler
async def handle_chat(user_id: int, user_input: str, db: AsyncSession):
    if not user_input.strip():
        return "Please enter a valid message."
    if is_medical_question(user_input):
        context = await update_context(db, user_id, user_input, "", max_turns=5)
        prompt_input = TEMPLATE.format(context=context, question=user_input)
        response = call_groq_model(prompt_input)
        # if not response or "Sorry" in response:
                # response = format_medical_response(user_input)

        response = bleach.clean(response, tags=['p', 'ul', 'li', 'h3', 'strong', '**', '*'], attributes={})
        await update_context(db, user_id, user_input, response, max_turns=5)
        return response
    # return format_medical_response(user_input)

def clear_chat():
    return "Chat history has been cleared. How can I assist you now?"






# # Determine if input is medical-related
# def is_medical_question(user_input, threshold=0.5):
#     if not core_terms:
#         logging.warning("Medical terms list is empty.")
#         return False
#     user_doc = nlp(user_input.lower())
#     return any(user_doc.similarity(term_doc) > threshold for term_doc in core_terms)

# # Maintain conversation context
# def update_context(context, user_input, response, max_turns=5):
#     lines = context.strip().split('\n') if context else []
#     lines += [f"User: {user_input}", f"AI: {response}"]
#     return '\n'.join(lines[-2 * max_turns:])  # Last n turns

# # Initialize conversation context
# context = ""

# def clear_chat():
#     global context
#     context = ""
#     return "Chat history has been cleared. How can I assist you now?"


# # Main chat handler
# def handle_chat(user_input):
#     global context
#     if not user_input.strip():
#         return "Please enter a valid message."
    
#     if is_medical_question(user_input):
#         prompt_input = TEMPLATE.format(context=context, question=user_input)
#         response = call_groq_model(prompt_input)

#         # Use fallback template only if model response is empty or invalid
#         if not response or "Sorry" in response:
#             response = format_medical_response(user_input)


#     context = update_context(context, user_input, response)
#     return response
