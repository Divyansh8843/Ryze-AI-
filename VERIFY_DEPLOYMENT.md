# 🚀 Ryze AI Service Verification Checklist

Since the architecture involves three separate services (Frontend, Backend, AI Service), correct configuration is **critical**.

## 1. 🐍 AI Service (Python)
**Status**: ✅ Code optimized for lightweight deployment.
**Changes Made**:
- Removed heavy libraries (`scikit-learn`, `numpy`) to prevent memory crashes.
- Added Robust Error Handling.
- Added Root (`/`) route for health checks.
- set `WEB_CONCURRENCY` and `TIMEOUT` in Procfile.

**👉 YOUR ACTION REQUIRED:**
1. **Redeploy** this service on Render.
2. Note the URL (e.g., `https://ryze-ai-service.onrender.com`).
3. Visit the URL in your browser. You should see: `{"message": "Ryze AI Service Running", ...}`.

## 2. ⚙️ Backend Service (Node.js)
**Status**: ✅ Logging added to debug connections.
**Changes Made**:
- Added logging to print the target `AI_SERVICE_URL`.
- Added Timeout handling.

**👉 YOUR ACTION REQUIRED:**
1. Go to your **Render Dashboard** -> **Backend Service** -> **Environment**.
2. **CRITICAL**: Check `AI_SERVICE_URL`.
   - It MUST be set to the URL of your AI Service (from Step 1).
   - Example: `https://ryze-ai-service.onrender.com` (No trailing slash).
   - If it is `http://localhost:5001`, **CHANGE IT**.
3. Redeploy the Backend.

## 3. 🖥️ Frontend (React)
**Status**: ✅ Configured to talk to Backend.
**Changes Made**: None needed (automatically detects VITE_API_URL).

**👉 YOUR ACTION REQUIRED:**
1. Ensure `VITE_API_URL` in your Vercel/Render Frontend Environment variables points to your **Backend Service** (e.g., `https://ryze-backend.onrender.com`).

---

## 🛑 If you still see 500 Errors:
1. Open the **Backend Service Logs** on Render.
2. Look for the log line: `[Node] Target URL: ...`.
3. If it says `localhost`, your environment variable is wrong.
4. If it says the correct URL but fails with 502, check the **AI Service Logs** for crashes.
