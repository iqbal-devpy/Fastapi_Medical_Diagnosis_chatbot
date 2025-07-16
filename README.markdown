# Medical Chatbot

## Overview

Medical Chatbot is a FastAPI-based web application designed to provide users with medical information and advice through an interactive chat interface. The application integrates with the Groq API for natural language processing, uses spaCy for medical term detection, and stores conversation history in a MySQL database. It includes user authentication, session management, and a responsive UI with dark mode support.

## Features

- **Medical Query Handling**: Processes user inputs to provide tailored medical advice using the Groq API.
- **Context-Aware Responses**: Maintains conversation history for contextual responses.
- **Database Integration**: Stores chat history in a MySQL database using SQLAlchemy.
- **Natural Language Processing**: Uses spaCy to identify medical-related queries.
- **Responsive UI**: Built with Jinja2 templates, featuring a chat interface and dark mode toggle.
- **Logging**: Comprehensive logging for debugging and monitoring.

## Project Structure

- `chatbot.py`: Core logic for handling chat interactions, Groq API calls, and medical term detection.
- `main.py`: FastAPI application setup, routes for chat, dashboard, and authentication.
- `database.py`: Configures the async MySQL database connection using SQLAlchemy.
- `models.py`: Defines SQLAlchemy models for `User` and `Chat` tables.
- `init_db.py`: Initializes the database schema asynchronously.
- `init_db_sync.py`: Synchronous version of database initialization.
- `base.py`: Base class for SQLAlchemy models.
- `medical_term.txt`: List of medical terms for spaCy to detect medical queries.
- `requirements.txt`: Python dependencies for the project.
- `templates/`: Jinja2 templates for the web interface (e.g., `index.html`, `dashboard.html`).
- `static/`: Static files (CSS, JavaScript) for the frontend.
- `logs/`: Directory for log files (`app.log`, `chatbot.log`, `init_db.log`, `init_db_sync.log`).

## Prerequisites

- Python 3.8+
- MySQL server
- Groq API key
- spaCy model (`en_core_web_md`)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd medical-chatbot
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy Model**:

   ```bash
   python -m spacy download en_core_web_md
   ```

5. **Configure Environment Variables**: Create a `.env` file in the project root with the following:

   ```env
   DATABASE_URL=mysql+aiomysql://<username>:<password>@localhost:3306/chatbot_db
   GROQ_API_KEY=<your-groq-api-key>
   SESSION_SECRET=<your-session-secret>
   MYSQL_USER=<mysql-username>
   MYSQL_PASSWORD=<mysql-password>
   MYSQL_DATABASE=chatbot_db
   ```

6. **Initialize the Database**:

   ```bash
   python inti_db.py
   ```

   Alternatively, for synchronous initialization:

   ```bash
   python init_db_sync.py
   ```

## Running the Application

1. **Start the FastAPI Server**:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access the Application**: Open a browser and navigate to `http://localhost:8000`.

## Usage

- **Home Page (**`/`**)**: Displays the chat interface where users can input medical queries.
- **Chat (**`/chat`**)**: Submit a message to receive a response from the Groq-powered chatbot.
- **Dashboard (**`/dashboard`**)**: View chat history for the logged-in user.
- **Toggle Dark Mode (**`/toggle_dark_mode`**)**: Switch between light and dark themes.
- **Clear Chat (**`/clear_chat`**)**: Mark chat history as deleted for the current user.

## API Endpoints

- `GET /`: Render the main chat interface.
- `POST /chat`: Process user messages and return bot responses.
- `POST /clear_chat`: Clear chat history.
- `GET /dashboard`: Display user-specific chat history.
- `POST /toggle_dark_mode`: Toggle dark mode.
- Session management is handled via `SessionMiddleware`.

## Logging

- Logs are stored in the `logs/` directory (`app.log`, `chatbot.log`, `init_db.log`, `init_db_sync.log`).
- Logs include server activities, chat interactions, and database initialization events.

## Notes

- **Security**: Ensure `SESSION_SECRET` is a strong, unique key in production.
- **Database**: Replace `DATABASE_URL` credentials with your MySQL configuration.
- **Groq API**: Obtain an API key from Groq and add it to the `.env` file.
- **Medical Advice**: The chatbot provides general guidance only. Always consult a healthcare professional for medical advice.

## Troubleshooting

- **Database Connection Issues**: Verify MySQL server is running and credentials in `.env` are correct.
- **Groq API Errors**: Check the API key and ensure the Groq service is accessible.
- **spaCy Errors**: Ensure the `en_core_web_md` model is installed.
- **Logs**: Check log files in the `logs/` directory for detailed error messages.

## Future Improvements

- Enhance authentication with OAuth support (e.g., Google login).
- Add real-time chat updates using WebSockets.
- Improve medical term detection with a larger dataset.
- Implement input validation for user messages.
- Add support for multilingual queries.

## License

This project is licensed under the MIT License.