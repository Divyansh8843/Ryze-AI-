# Ryze AI: Deterministic UI Generator Agent

![Ryze AI Banner](https://capsule-render.vercel.app/api?type=waving&height=250&color=gradient&text=RYZE%20AI&desc=Deterministic%20UI%20Generation%20Agent&animation=fadeIn&fontAlign=50&fontAlignY=40)

[![Status](https://img.shields.io/badge/Status-Submission%20Ready-success?style=for-the-badge&logo=rocket)](https://ryze-ai-agent.vercel.app)
[![Architecture](https://img.shields.io/badge/Architecture-Heuristic%20Agent-blueviolet?style=for-the-badge&logo=python)](https://github.com/Divyansh8843/Ryze-AI-)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

## 📋 Project Overview
**Ryze AI** is an autonomous, deterministic AI agent designed to convert natural language into working, production-ready UI code. Built to simulate the capabilities of tools like **Claude Code**, Ryze prioritizes **safety, reproducibility, and visual consistency** over open-ended generation.

This project was built as a **72-hour time-boxed assignment** to demonstrate:
- **Agentic Workflow**: Planner → Generator → Explainer.
- **Deterministic UI**: A fixed, robust component system.
- **Iterative Refinement**: Modifying code without breaking it.

---

## 🏗️ Architecture
Ryze AI follows a strictly decoupled microservices architecture:

1.  **Frontend (React + Vite)**:
    - **Dual-Pane IDE**: Chat interface on the left, Code/Preview on the right.
    - **Live Compiler**: Uses `@babel/standalone` to render React code in the browser securely.
    - **Sandboxed Execution**: Prevents CSS leakage and ensures style isolation.

2.  **Gateway (Node.js + Express)**:
    - **API Orchestration**: Proxies requests to the AI Engine.
    - **Persistence Layer**: MongoDB storage for deployment history and user sessions.
    - **Deployment Manager**: Generates standalone HTML artifacts for global sharing.

3.  **AI Engine (Python + Flask)**:
    - **The "Brain"**: A deterministic heuristic engine (Symbolic NLP).
    - **No Hallucinations**: Uses rule-based entity extraction and template mapping instead of probabilistic LLM token generation for core structural logic.
    - **State Awareness**: capable of parsing existing code and injecting new components contextually.

---

## 🤖 Agent Design
The core "AI" is implemented not as a black-box LLM, but as a transparent, multi-step agent:

### Step 1: 🧠 Planner
- **Intent Classification**: Analyzes the prompt to classify it into categories (e.g., `dashboard`, `landing_page`, `login`).
- **Entity Extraction**: Identifies key design tokens:
  - **Colors**: "Make it *emerald*" → `emerald-500`
  - **Brand Name**: "Call it *FinTech Pro*" → `FinTech Pro`
  - **Components**: "Add a *sidebar*" → `Sidebar` injection flag.

### Step 2: ⚙️ Generator
- **Template Selection**: Fetches the validated, accessible base template for the detected intent.
- **Token Injection**: Fills the template with extracted entities (e.g., replacing `{{PRIMARY_COLOR}}` with `emerald`).
- **Component Composition**: Assembles the view using the **Fixed Component Library**.

### Step 3: 🗣️ Explainer
- **Reasoning Output**: Generates a human-readable explanation of *why* specific decisions were made.
- **Plan Visualization**: Returns the structured plan (e.g., "1. Detected Intent: Dashboard. 2. Applied Theme: Emerald.").

---

## 🧩 Component System Design
To satisfy the **Core Constraint**, Ryze AI uses a **Strict Component Library**. The AI *cannot* write arbitrary HTML or CSS classes. It must use:

- **`<Button />`**: Standardized interactive element.
- **`<Card />`**: Container for grouping content.
- **`<Input />`**: User data entry.
- **`<Table />`**: structured data display.
- **`<Navbar />`**: Consistent top-level navigation.
- **`<Sidebar />`**: Vertical navigation pattern.
- **`<Chart />`**: Data visualization (Mocked).

**Constraint Enforcement**:
The Python engine's regex operations are tuned to only inject these specific component strings. The Frontend's Babel scope *only* exposes these components, ensuring that any hallucinated component would result in a clear error (or no render), forcing correctness.

---

## 🔄 Iteration & Modification
Ryze AI supports **Incremental Edits**. It does NOT regenerate the entire file on every turn.

**Example Flow**:
1.  **User**: "Create a blue dashboard."
    - **Agent**: Generates full `Dashboard` code with `blue-600` theme.
2.  **User**: "Make it dark node and add a sidebar."
    - **Agent**:
        - Parses existing code.
        - **Regex Swap**: Updates global theme tokens.
        - **Injection**: Locates the layout wrapper and inserts `<Sidebar />` without touching the inner content.
        - **Result**: The original data/structure is preserved; only the requested changes are applied.

---

## 🚀 Known Limitations & Tradeoffs
- **Heuristic NLP**: The current NLP engine is rule-based. It excels at specific keywords ("dashboard", "blue", "add footer") but may struggle with abstract nuances like "make it feel more cozy".
- **Template Rigidity**: The layout structure is robust but finite. It cannot invent entirely new layout paradigms outside its template library.
- **Regex Parsing**: Iterative modification relies on regex matching. Highly complex, nested code structures might occasionally confuse the insertion logic.

## 🔮 Future Improvements
With more time, I would implement:
1.  **AST Parsing (Abstract Syntax Tree)**: Replace regex with real AST manipulation (e.g., using `libcst` in Python) for surgical code edits.
2.  **LLM "Function Calling"**: Integrate a real LLM (e.g., GPT-4o) specifically for the *Planner* step to handle abstract intents, while keeping the *Generator* deterministic.
3.  **Component Props Schema**: A strict JSON schema ensuring every generated prop is valid against the component definition.

---

## 📦 Setup & Deployment

1.  **Clone**: `git clone https://github.com/Divyansh8843/Ryze-AI-.git`
2.  **Backend**: `cd backend && npm install && npm start`
3.  **AI Service**: `cd ai-service && pip install flask flask-cors && python app.py`
4.  **Frontend**: `cd frontend && npm install && npm run dev`

**Deployed URL**: [https://ryze-ai-agent.vercel.app](https://ryze-ai-agent.vercel.app)

---
*Submitted by Divyansh for Ryze AI Assignment.*
