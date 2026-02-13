## 🚀 Vercel Deployment Checklist (Critical)

1.  **Environment Variables (Settings -> Environment Variables)**:
    - `VITE_API_URL`: **`https://your-node-backend.onrender.com/api/generator`**
      *(Must include `https://` and `/api/generator`)*

2.  **Verify CORS (Render Backend)**:
    - Ensure `FRONTEND_URL` on Render is set to: `https://ryze-ai-agent.vercel.app`
    - (I have already hardcoded this domain in `server.js` as a backup, but Env Var is best practice).

3.  **Deploy**:
    - Push changes to GitHub.
    - Vercel will auto-deploy.
    - Check Vercel Logs if build fails.

4.  **Testing**:
    - Open `https://ryze-ai-agent.vercel.app`
    - Open Browser Console (F12) -> Check for "✅ Backend Connected".
    - If you see "Production API URL: <URL>", verify it looks correct.
