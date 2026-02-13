## Deployment Guide (Vercel + Render)

### 1. Backend (Already Deployed on Render?)
Ensure your Node.js Backend is running on Render and accessible.
- **URL**: `https://your-node-backend.onrender.com` (Example)
- **Environment Variables** (on Render):
    - `AI_SERVICE_URL`: `https://ryze-ai-service.onrender.com` (Your Python Microservice)
    - `FRONTEND_URL`: `https://your-vercel-app.vercel.app` (Add this AFTER deploying Frontend)
    - `MONGO_URI`: Your MongoDB Connection String

### 2. Frontend (Deploy to Vercel)
1.  Push your code to **GitHub**.
2.  Go to **Vercel Dashboard** -> **New Project**.
3.  Import the `frontend` directory (Important: Root Directory should be `frontend`).
4.  **Build Settings**:
    - Framework: Vite
    - Build Command: `npm run build`
    - Output Directory: `dist`
5.  **Environment Variables** (in Vercel Project Settings):
    - `VITE_API_URL`: `https://your-node-backend.onrender.com/api/generator`
      *(Note: Specifically pointing to the generator route base, matching your local setup logic)*

### 3. Final Wiring
Once Vercel gives you the domain (e.g., `ryze-ai.vercel.app`):
1.  Go back to **Render (Node Backend)**.
2.  Update `FRONTEND_URL` to `https://ryze-ai.vercel.app`.
3.  Redeploy/Restart the Node Backend.

### Troubleshooting
- **CORS Errors**: Check `FRONTEND_URL` on Render matching your Vercel domain exactly (no trailing slash).
- **Network Errors**: Check `VITE_API_URL` on Vercel. It must start with `https://`.
