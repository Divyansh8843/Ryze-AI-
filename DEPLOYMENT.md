# 🚀 Deployment Guide

This repository is designed for a **Microservices Architecture** deployment.
You have three main components to deploy:

1.  **Frontend** (React + Vite)
2.  **API Gateway** (Node.js + Express)
3.  **AI Engine** (Python + Flask)

---

## 🏗️ Option 1: Render.com (Recommended for Free Tier)

Render allows you to deploy all three services easily.

### 1. Deploy the AI Engine (Python)
1.  Create a new **Web Service**.
2.  Connect your GitHub repository.
3.  **Root Directory**: `ai-service`
4.  **Runtime**: Python 3
5.  **Build Command**: `pip install -r requirements.txt`
6.  **Start Command**: `gunicorn app:app` (or `python app.py` for dev)
7.  **Environment Variables**:
    -   `PORT`: `10000` (Render default) or `5001`
8.  **Copy the Service URL** (e.g., `https://ryze-ai-engine.onrender.com`).

### 2. Deploy the API Gateway (Node.js)
1.  Create a new **Web Service**.
2.  Connect your GitHub repository.
3.  **Root Directory**: `backend`
4.  **Runtime**: Node
5.  **Build Command**: `npm install`
6.  **Start Command**: `node server.js`
7.  **Environment Variables**:
    -   `AI_SERVICE_URL`: The URL from Step 1 (e.g., `https://ryze-ai-engine.onrender.com`)
    -   `PORT`: `10000` (Render default) or `5000`
8.  **Copy the Service URL** (e.g., `https://ryze-api-gateway.onrender.com`).

### 3. Deploy the Frontend (React)
1.  Create a new **Static Site**.
2.  Connect your GitHub repository.
3.  **Root Directory**: `frontend`
4.  **Build Command**: `npm run build`
5.  **Publish Directory**: `dist`
6.  **Environment Variables**:
    -   `VITE_API_URL`: The URL from Step 2 (e.g., `https://ryze-api-gateway.onrender.com/api/generator`)

---

## ⚡ Option 2: Heroku (Monorepo)

This project includes a `Procfile` for Heroku deployment.

1.  Install Heroku CLI and login.
2.  Initialize a git repo if not already done.
3.  Create a Heroku app: `heroku create ryze-ai-app`
4.  Add buildpacks for both Node and Python:
    ```bash
    heroku buildpacks:add heroku/nodejs
    heroku buildpacks:add heroku/python
    ```
5.  Push to Heroku: `git push heroku main`
6.  Scale dynos: `heroku ps:scale web=1 ai=1`

---

## 🏠 Option 3: Local Development (Docker-ready)

1.  Install dependencies: `npm run install-all`
2.  Start everything: `npm run dev`
3.  Access at `http://localhost:5173`

---

## 🛡️ Production Checklist

-   [ ] Ensure `NODE_ENV` is set to `production` in backend.
-   [ ] Verify `AI_SERVICE_URL` points to the correct Python service.
-   [ ] Verify `VITE_API_URL` excludes trailing slashes if necessary (the code handles it, but good practice).
-   [ ] Enable **HTTPS** on all services (Render/Vercel handles this automatically).
