Backend for StyleAgent

Quick start

1. Create and activate venv (optional)
   python3 -m venv .venv && source .venv/bin/activate

2. Install requirements
   pip install -r requirements.txt

3. Run the server
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

API Endpoints

- GET /health: Health check
- POST /api/chat: Basic chat stub
- POST /api/analyze: Image analysis stub
- POST /api/recommend: Return outfit recommendations matching frontend types

Notes

- CORS is open to all origins for local development. Configure env var ALLOWED_ORIGINS in production.
- The API currently returns mock data aligned with the frontend. Replace with real models as you build the pipeline.

