# Deployment Guide (Streamlit Frontend + Render Backend)

## 1) Install dependencies locally

Frontend-only (for Streamlit app):

pip install -r requirements.txt

Backend-only (for Render API parity):

pip install -r requirements-backend.txt

## 2) Run locally

Backend API:

uvicorn api.app:app --host 0.0.0.0 --port 8000

Frontend dashboard:

streamlit run frontend/dashboard.py

## 3) Environment variables

Backend (Render):
- FRONTEND_URL=https://<your-streamlit-app>.streamlit.app
- Optional: ALLOWED_ORIGINS=https://<your-streamlit-app>.streamlit.app,http://localhost:8501
- Optional: API_KEY=<same-secret-used-by-frontend>

Frontend (Streamlit Cloud secrets):
- API_URL=https://<your-render-api>.onrender.com
- Optional: API_KEY=<same-secret-used-by-backend>
- DASHBOARD_USERNAME=admin
- DASHBOARD_PASSWORD=<strong-password>

## 4) Deploy backend on Render

1. Connect repository in Render.
2. Use Blueprint from render.yaml or create Web Service manually.
3. Build command:

pip install -r requirements-backend.txt

4. Start command:

uvicorn api.app:app --host 0.0.0.0 --port $PORT

## 5) Deploy frontend on Streamlit Cloud

1. Create app from this repo.
2. App file path: frontend/dashboard.py
3. Add Secrets in Streamlit Cloud with API_URL and dashboard credentials.
4. If backend API_KEY is enabled, also add API_KEY with same value.

## 6) Verify

1. Backend health: GET / should return status API running.
2. Frontend loads and charts show data.
3. Live Monitor updates without local CSV dependency.
