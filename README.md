# AI-Ticket-Automation
Event-driven AI ticket automation system using FastAPI, LangChain, and OpenAI for automated triage and response generation.

This project demonstrates real-world IT automation using FastAPI, REST APIs, API key authentication, SQLite, LangChain, and OpenAI — similar to how managed IT and internal operations platforms automate manual workflows.
---------------------------------------------------------------------------------------------------------------------------------------------
Features:
** RESTful API (GET, POST, PATCH)

** API Key authentication (X-API-Key)

** Event-driven background processing (no polling)

** LangChain integration with OpenAI

** SQLite database (lightweight local storage)

** Error handling with status tracking

** Swagger UI for testing
-----------------------------------------------------------------------------------------------------------------------------------------------
Installation (Windows)
1. Clone the repository
    git clone https://github.com/your-username/ai-ticket-automation.git
    cd ai-ticket-automation
2. Create virtual environment
    python -m venv .venv
    .\.venv\Scripts\activate
3. Install dependencies
    pip install -r requirements.txt
----------------------------------------------------------------------------------------------------------------------------------------------
Environment Variables

Create a .env file in the project root:

API_KEY=your_internal_api_key
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
BASE_URL=http://127.0.0.1:8000
------------------------------------------------------------------------------------------------------------------------------------------------
Run the Application
uvicorn app.main:app --reload

Swagger UI for easy testing

http://127.0.0.1:8000/docs

------------------------------------------------------------------------------------------------------------------------------------------------


Event-Driven Processing Flow
Client → POST /tickets
        ↓
Database (status = NEW)
        ↓
FastAPI Background Task
        ↓
LangChain + OpenAI
        ↓
Update ticket → PROCESSED Ticket With AI Summary + Draft Reply 

