# 🏃‍♂️ How to Run Ryze AI on Localhost

This project uses a **Microservices Architecture**. You need to run 3 separate services (Frontend, Backend, AI Engine).

We have streamlined this into a single command, but here are the detailed steps to ensure everything works 100%.

## 🔧 Prerequisites

1.  **Node.js**: v18 or higher installed.
2.  **Python**: v3.10 or higher installed.
3.  **MongoDB**: Installed and running locally (default port 27017).
    -   *If you don't have MongoDB installed, the app will still work but won't save logs.*

## 🚀 One-Click Start (Windows)

1.  **Double-click `START_RYZE.bat`** in the root folder.
2.  It will:
    -   Clean previous caches (Frontend/Backend) to prevent errors.
    -   Install dependencies for all 3 services.
    -   Launch everything concurrently.

## 🐢 Manual Start (Mac/Linux/Windows)

If you prefer the command line:

1.  Open a terminal in the project root folder.
2.  Run the installation script:
    ```bash
    npm run install-all
    ```
    *This installs dependencies for Frontend (React), Backend (Node), and AI Service (Python) all at once.*

3.  Start the application:
    ```bash
    npm run dev
    ```
    *This uses `concurrently` to launch all 3 services.*

4.  **Open your browser**:
    -   Go to [http://localhost:5173](http://localhost:5173) to uses the app.

---

## 🔍 Troubleshooting

-   **Error: `python` not found**: Try using `python3` or `py` depending on your OS.
-   **Error: `Module not found`**: Ensure you ran `npm install` in the specific folder.
-   **MongoDB Connection Error**: Ensure MongoDB service is started (`mongod`).
-   **Port in Use**: Check if ports 3000, 5000, or 5001 are already taken.
