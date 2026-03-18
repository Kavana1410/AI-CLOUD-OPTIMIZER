# Deployment Guide (Free Streamlit-Only First)

## 1) Zero-card free deployment (recommended)

Use Streamlit Community Cloud only. The app can run simulations locally inside Streamlit and does not require a backend.

### Steps

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from this repo.
4. Set app file path to `frontend/dashboard.py`.
5. Add Streamlit secrets:

```
DASHBOARD_USERNAME = "admin"
DASHBOARD_PASSWORD = "change_me"
```

6. Deploy and open the app URL.

### Optional API mode later

If you later add a backend, set:

```
API_URL = "https://your-backend-url"
API_KEY = "your_api_key"
```

Without `API_URL`, the dashboard automatically runs local simulation mode.

## 2) Local run

```
pip install -r requirements.txt
streamlit run frontend/dashboard.py
```

## 3) Optional backend deployment (not required for free mode)

Backend files are kept for future split deployment:

- `api/app.py`
- `render.yaml`
- `requirements-backend.txt`

## 4) Verify

1. Login page appears.
2. Dashboard loads strategy metrics.
3. Live Monitor updates without needing API_URL.
