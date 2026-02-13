import time
from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from flask_cors import CORS
from logic.nlp_engine import classifier, style_extractor
from logic.templates import TEMPLATES_MAP, PRICING_SECTION_SNIPPET

FRONTEND_URL = os.getenv("FRONTEND_URL")

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "engine": "Symbolic NLP"}), 200

@app.route('/generate', methods=['POST'])
def generate_ui():
    """
    Main endpoint for AI UI Generation.
    Receives: { "prompt": "Create a red dashboard..." }
    Returns: { "plan": "...", "code": "...", "explanation": "..." }
    """
    start_time = time.time()
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # 1. Intent Classification (AI Fundamentals)
    intent = classifier.predict(prompt)
    
    # 2. Entity Extraction (Rule-based NLP)
    primary_color = style_extractor.extract_primary_color(prompt)
    brand_name = style_extractor.extract_brand_name(prompt)
    
    # 3. Template Selection & Filling (Deterministic Generation)
    raw_template = TEMPLATES_MAP.get(intent, TEMPLATES_MAP['dashboard'])
    
    # Simple Jinja-like replacement
    generated_code = raw_template.replace("{{PRIMARY_COLOR}}", primary_color)
    generated_code = generated_code.replace("{{BRAND_NAME}}", brand_name)
    
    # 4. Construct Response
    processing_time = round((time.time() - start_time) * 1000, 2)
    
    explanation = (
        f"I analyzed your request using a Symbolic NLP engine.\n"
        f"- **Intent Detected**: {intent.capitalize()} (Based on keyword frequency)\n"
        f"- **Style Extraction**: Primary Color = '{primary_color}', Brand = '{brand_name}'\n"
        f"- **Architecture**: Selected the optimal {intent} layout pattern from the deterministic library.\n"
        f"- **Processing Time**: {processing_time}ms"
    )

    plan = (
        f"1. **Analyze Intent**: '{prompt}' -> {intent}\n"
        f"2. **Extract Entities**: Color: {primary_color}, Brand: {brand_name}\n"
        f"3. **Select Template**: {intent}_v1.0.js\n"
        f"4. **Compile**: Inject variables and validate structure."
    )

    return jsonify({
        "plan": plan,
        "code": generated_code,
        "explanation": explanation,
        "meta": {
            "intent": intent,
            "processing_time_ms": processing_time
        }
    })

@app.route('/modify', methods=['POST'])
def modify_ui():
    """
    Endpoint for iterative refinement.
    Receives: { "prompt": "Make it green", "currentCode": "..." }
    """
    data = request.json
    prompt = data.get('prompt', '')
    current_code = data.get('currentCode', '')
    
    if not prompt or not current_code:
        return jsonify({"error": "Prompt and currentCode are required"}), 400

    # 1. Extract new style attributes
    new_color = style_extractor.extract_primary_color(prompt)
    
    # 2. Apply modifications (Symbolic replacements)
    # This is a naive implementation but robust for the demo.
    # It replaces color classes.
    # Regex replacement for robust color swapping
    import re
    
    # Replace simple color names in text/bg classes
    # Expanded palette to catch all Tailwind colors
    known_colors = [
        'slate', 'gray', 'zinc', 'neutral', 'stone',
        'red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 
        'cyan', 'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose'
    ]
    
    # Regex to find existing color classes (e.g. bg-blue-500, from-indigo-600)
    # Group 1: Prefix (bg, text, etc)
    # Group 2: Color name
    # Group 3: Shade (100-900)
    pattern = r'\b(bg|text|border|ring|from|to|via|shadow|decoration)-(' + '|'.join(known_colors) + r')-(\d+)\b'
    
    def replacer(match):
        prefix = match.group(1)
        shade = match.group(3)
        # Construct new class with the requested color
        return f"{prefix}-{new_color}-{shade}"

    modified_code = re.sub(pattern, replacer, current_code)

    explanation_steps = [
        f"- Updated theme color tokens across the component tree to '{new_color}'.",
    ]
    high_level_plan = [
        f"1. Detected iterative style change request in: '{prompt}'.",
        f"2. Swapped Tailwind color tokens to '{new_color}' while preserving layout and component structure.",
    ]

    lower_prompt = prompt.lower()
    
    # --- Advanced Heuristics (Simulated AI Agent) ---

    # 3. Add Navbar
    if ("navbar" in lower_prompt or "navigation" in lower_prompt) and "<Navbar" not in modified_code:
        nav_snippet = '<Navbar brand="Ryze App" links={[{label:"Home", href:"#"}, {label:"Features", href:"#"}, {label:"Pricing", href:"#"}]} user={{name:"User", avatar:"https://github.com/shadcn.png"}} className="mb-8" />\n'
        # Insert after opening div if possible
        if "return (" in modified_code:
            # Try to insert after the first div opening
            pass # Complex to parse, let's prepend to the first <div> inside return
            modified_code = modified_code.replace("return (", "return (\n<div className=\"min-h-screen bg-gray-50 dark:bg-black\">\n" + nav_snippet, 1)
            modified_code = modified_code.replace(");", "</div>\n);", 1) # Close the wrapper
        else:
             # Fallback
             pass
        high_level_plan.append("3. Injected Navigation Bar component with responsive layout.")
        explanation_steps.append("- Added <Navbar> component to the top of the view hierarchy.")

    # --- BONUS INTELLIGENCE PACK (Global Launch Ready) ---

    # 3b. Add Hero Section
    if ("hero" in lower_prompt or "banner" in lower_prompt) and "<h1>" not in modified_code and "Welcome" not in modified_code:
        hero_snippet = '<div className="py-20 text-center bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-black"><h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">Build Faster with AI</h1><p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">The most advanced platform for deploying web applications instantly.</p><div className="flex justify-center gap-4"><Button className="rounded-full px-8 py-6 text-lg">Get Started</Button><Button className="rounded-full px-8 py-6 text-lg bg-white text-gray-900 border hover:bg-gray-50">Learn More</Button></div></div>'
        # Intelligent Insertion: After Navbar if present, else top
        if "<Navbar" in modified_code:
             modified_code = modified_code.replace("/>", "/>\n" + hero_snippet, 1)
        elif "return (" in modified_code:
             # Insert inside the wrapper div we might have created for Navbar, or just after open div
             modified_code = modified_code.replace("className=\"min-h-screen bg-gray-50 dark:bg-black\">\n", "className=\"min-h-screen bg-gray-50 dark:bg-black\">\n" + hero_snippet + "\n", 1)
        high_level_plan.append("3. Generated conversion-optimized Hero Section.")
        explanation_steps.append("- Added gradient Hero section with CTAs.")

    # 3c. Add Features Section
    if ("features" in lower_prompt or "benefits" in lower_prompt) and "Feature 1" not in modified_code:
        feat_snippet = '<div className="py-16 px-6"><h2 className="text-3xl font-bold text-center mb-12">Why Choose Us</h2><div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto"><Card className="p-8 hover:shadow-lg transition-all"><window.Lucide.Zap className="w-10 h-10 text-yellow-500 mb-4" /><h3 className="text-xl font-bold mb-2">Lightning Fast</h3><p className="text-gray-500">Deploy in seconds, not minutes.</p></Card><Card className="p-8 hover:shadow-lg transition-all"><window.Lucide.Shield className="w-10 h-10 text-green-500 mb-4" /><h3 className="text-xl font-bold mb-2">Secure by Default</h3><p className="text-gray-500">Enterprise-grade security built-in.</p></Card><Card className="p-8 hover:shadow-lg transition-all"><window.Lucide.Globe className="w-10 h-10 text-blue-500 mb-4" /><h3 className="text-xl font-bold mb-2">Global Scale</h3><p className="text-gray-500">Run your app on the edge.</p></Card></div></div>'
        # Insert after Hero if present, else generic
        if "Build Faster with AI" in modified_code:
             modified_code = modified_code.replace("</div></div>", "</div></div>\n" + feat_snippet, 1)
        elif "<Navbar" in modified_code:
             modified_code = modified_code.replace("/>", "/>\n" + feat_snippet, 1)
        else:
             # Fallback: append
             if "</main>" in modified_code:
                 modified_code = modified_code.replace("</main>", feat_snippet + "\n</main>", 1)
        high_level_plan.append("3. Added Features Grid with hover effects.")
        explanation_steps.append("- Created 3-column Features section using Card components.")

    # 3d. Add Footer
    if ("footer" in lower_prompt) and "<footer" not in modified_code:
        footer_snippet = '<footer className="py-8 text-center text-gray-500 border-t dark:border-gray-800 mt-12"><p>© 2024 Ryze AI. All rights reserved.</p><div className="flex justify-center gap-4 mt-4 text-sm"><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Twitter</a></div></footer>'
        if "</main>" in modified_code:
             modified_code = modified_code.replace("</main>", footer_snippet + "\n</main>", 1)
        elif "</div>\n);" in modified_code:
             modified_code = modified_code.replace("</div>\n);", footer_snippet + "\n</div>\n);", 1)
        high_level_plan.append("3. Appended professional Footer.")
        explanation_steps.append("- Added clean Footer with copyright and links.")


    # 3e. Add Testimonials (Social Proof)
    if ("testimonials" in lower_prompt or "reviews" in lower_prompt) and "user says" not in modified_code:
        testi_snippet = '<div className="py-20 bg-gray-50 dark:bg-gray-900/50"><h2 className="text-3xl font-bold text-center mb-12">Trusted by Developers</h2><div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto px-6"><Card className="p-6"><p className="italic text-gray-600 mb-4">"Ryze AI changed how we ship software. Absolutely incredible."</p><div className="flex items-center gap-3"><div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center font-bold text-blue-600">JD</div><div><div className="font-bold">John Doe</div><div className="text-sm text-gray-500">CTO, TechCorp</div></div></div></Card><Card className="p-6"><p className="italic text-gray-600 mb-4">"The best AI coding assistant I have ever used. Highly recommended."</p><div className="flex items-center gap-3"><div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center font-bold text-purple-600">AS</div><div><div className="font-bold">Alice Smith</div><div className="text-sm text-gray-500">Lead Dev, StartupInc</div></div></div></Card></div></div>'
        # Insert before footer if present
        if "<footer" in modified_code:
             modified_code = modified_code.replace("<footer", testi_snippet + "\n<footer", 1)
        elif "</main>" in modified_code:
             modified_code = modified_code.replace("</main>", testi_snippet + "\n</main>", 1)
        high_level_plan.append("3. Added Social Proof section with user testimonials.")
        explanation_steps.append("- Created trusted Testimonials grid.")

    # --- ULTRA-ADVANCED: Full App Orchestrator ---
    if ("full app" in lower_prompt or "complete website" in lower_prompt or "landing page" in lower_prompt) and "<Navbar" not in modified_code:
         # Trigger all sections if not present
         # This effectively chains the logic by appending keywords to the prompt internally? 
         # No, prompt is fixed. We must force inject.
         
         # Force Inject Navbar (if not present)
         if "<Navbar" not in modified_code:
             # Logic same as above
             nav_snippet = '<Navbar brand="Ryze Enterprise" links={[{label:"Platform", href:"#"}, {label:"Solutions", href:"#"}, {label:"Pricing", href:"#"}]} user={{name:"Admin", avatar:"https://github.com/shadcn.png"}} className="sticky top-0 z-50" />\n'
             if "return (" in modified_code:
                 modified_code = modified_code.replace("return (", "return (\n<div className=\"min-h-screen bg-gray-50 dark:bg-black font-sans text-gray-900 dark:text-gray-100\">\n" + nav_snippet, 1)
                 # Only close if we haven't already unwrapped?
                 # Assume standard template structure.
                 if "</div>\n);" not in modified_code: modified_code = modified_code.replace(");", "</div>\n);", 1)

         # Force Inject Hero
         if "Welcome" not in modified_code:
             hero_snippet = '<div className="py-24 text-center"><h1 className="text-6xl font-extrabold mb-6 tracking-tight">Ship Your Idea <span className="text-blue-600">Today</span></h1><p className="text-2xl text-gray-500 mb-10 max-w-3xl mx-auto">Ryze AI generates production-ready full-stack applications in seconds.</p><button className="px-8 py-4 bg-black dark:bg-white text-white dark:text-black rounded-full text-lg font-bold hover:opacity-80 transition-opacity">Start Building Free</button></div>'
             modified_code = modified_code.replace("/>\n", "/>\n" + hero_snippet + "\n", 1) # Append after Navbar
         
         # Force Inject Features
         if "Feature 1" not in modified_code:
              feat_snippet = '<div className="py-20 bg-white dark:bg-gray-900"><div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12 text-center"><div><div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6"><window.Lucide.Cpu className="w-8 h-8 text-blue-600" /></div><h3 className="text-xl font-bold mb-2">AI Powered</h3><p className="text-gray-500">Built on next-gen LLMs.</p></div><div><div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-6"><window.Lucide.Zap className="w-8 h-8 text-purple-600" /></div><h3 className="text-xl font-bold mb-2">Instant Deploy</h3><p className="text-gray-500">From prompt to production.</p></div><div><div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-6"><window.Lucide.Layers className="w-8 h-8 text-green-600" /></div><h3 className="text-xl font-bold mb-2">Full Stack</h3><p className="text-gray-500">React, Node, Python included.</p></div></div></div>'
              modified_code = modified_code.replace("</button></div>", "</button></div>\n" + feat_snippet, 1) # Append after Hero

         # Force Inject Footer
         if "<footer" not in modified_code:
             footer_snippet = '<footer className="py-12 border-t dark:border-gray-800 text-center text-gray-500"><p>&copy; 2026 Ryze AI Inc.</p></footer>'
             if "</main>" in modified_code: modified_code = modified_code.replace("</main>", footer_snippet + "\n</main>", 1)
             elif "</div>\n);" in modified_code: modified_code = modified_code.replace("</div>\n);", footer_snippet + "\n</div>\n);", 1)
         
         high_level_plan.append("3. ORCHESTRATOR: Assembled complete SaaS Landing Page architecture.")
         explanation_steps.append("- Generated Full-Stack Landing Page structure.")

    # 4. Add Sidebar (Existing)
    if ("sidebar" in lower_prompt or "drawer" in lower_prompt) and "<Sidebar" not in modified_code:
        # We need a layout wrapper
        sidebar_snippet = '<Sidebar items={[{label:"Dashboard", icon:"LayoutDashboard"}, {label:"Settings", icon:"Settings"}, {label:"Pro", icon:"Zap"}]} activeItem="Dashboard" className="h-screen hidden md:block" />'
        
        # Checking for main content wrapper
        if "className=\"min-h-screen" in modified_code:
             modified_code = modified_code.replace("className=\"min-h-screen", "className=\"min-h-screen flex", 1)
             modified_code = modified_code.replace("return (\n<div", "return (\n<div", 1) # Logic is tricky
             # Simplified: Just prepend sidebar to the first internal div
             # Let's assume standard structure: return ( <div ...> ... </div> )
             # We inject sidebar as first child of that div
             modified_code = re.sub(r'(<div[^>]*>)', r'\1\n' + sidebar_snippet, modified_code, count=1)
             high_level_plan.append("3. Integrated Sidebar navigation panel.")
             explanation_steps.append("- Added <Sidebar> component and updated layout to Flexbox 'row'.")

    # 5. Add Chart
    if ("chart" in lower_prompt or "graph" in lower_prompt) and "<Chart" not in modified_code:
         chart_snippet = '<div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-8"><Chart type="bar" color="' + new_color + '" /><Chart type="line" color="' + new_color + '" /></div>'
         # Insert before footer or end
         if "</main>" in modified_code:
             modified_code = modified_code.replace("</main>", chart_snippet + "\n</main>", 1)
         elif "</div>" in modified_code:
             # Insert before last div
             modified_code = modified_code[:modified_code.rfind("</div>")] + chart_snippet + "\n</div>"
         high_level_plan.append("3. Visualized data with interactive Charts.")
         explanation_steps.append("- Added Bar and Line <Chart> components.")

    # 6. Pricing Section (Existing Logic Refined)
    if "pricing" in lower_prompt and "section" in lower_prompt:
        if "RYZE_PRICING_SECTION" not in modified_code and "id=\"pricing\"" not in modified_code:
            insertion_target = "</main>"
            if insertion_target in modified_code:
                modified_code = modified_code.replace(insertion_target, PRICING_SECTION_SNIPPET + "\n" + insertion_target, 1)
            else:
                modified_code = modified_code.rstrip() + PRICING_SECTION_SNIPPET + "\n"
            high_level_plan.append("3. Inserted a deterministic Pricing section snippet before the main footer.")
            explanation_steps.append("- Added a structured pricing section using the shared component library.")

    plan_text = "\n".join(high_level_plan)
    explanation_text = "I performed a constrained iterative update:\n" + "\n".join(explanation_steps)

    return jsonify({
        "plan": plan_text,
        "code": modified_code,
        "explanation": explanation_text
    })


# Deployment Configuration
DEPLOY_DIR = "deployments"
if not os.path.exists(DEPLOY_DIR):
    os.makedirs(DEPLOY_DIR)

@app.route('/deploy', methods=['POST'])
def deploy_project():
    data = request.json
    code = data.get('code', '')
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    deployment_id = str(uuid.uuid4())[:8]
    filename = f"{deployment_id}.html"
    filepath = os.path.join(DEPLOY_DIR, filename)
    
    # Prepare code for standalone HTML
    lines = code.split('\n')
    # Filter imports
    clean_code = '\n'.join([l for l in lines if not l.strip().startswith('import ')])
    # Handle exports
    clean_code = clean_code.replace('export default function', 'function')
    clean_code = clean_code.replace('export default', '')
    
    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ryze Deployment {deployment_id}</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" href="data:,">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>body {{ margin: 0; background: #f0f2f5; font-family: sans-serif; }}</style>
</head>
<body>
    <div id="root"></div>

    <!-- Share Toolbar -->
    <div style="position: fixed; bottom: 24px; right: 24px; z-index: 10000; display: flex; align-items: center; gap: 12px; font-family: system-ui, -apple-system, sans-serif;">
        <button onclick="copyLink()" id="shareBtn" style="background: #ffffff; color: #000000; border: 1px solid #e5e7eb; padding: 8px 16px; border-radius: 9999px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-weight: 500; transition: all 0.2s; display: flex; align-items: center; gap: 6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            Share
        </button>
        <a href="http://localhost:5173" target="_blank" style="text-decoration: none;">
            <div style="background: #000000; color: #ffffff; padding: 8px 16px; border-radius: 9999px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-weight: 600; display: flex; align-items: center; gap: 6px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                Built with Ryze
            </div>
        </a>
    </div>
    <script>
        function copyLink() {{
            navigator.clipboard.writeText(window.location.href);
            const btn = document.getElementById('shareBtn');
            const original = btn.innerHTML;
            btn.innerHTML = 'Copied!';
            btn.style.background = '#e5e7eb';
            setTimeout(() => {{
                btn.innerHTML = original;
                btn.style.background = '#ffffff';
            }}, 2000);
        }}
    </script>

    <script type="text/babel">
        const {{ useState, useEffect, useRef }} = React;

        // --- Lucide React Adapter (Polyfill) ---
        // This bridges the gap between generated React code (expecting <Lucide.Icon />)
        // and the vanilla Lucide library loaded via CDN.
        const Lucide = new Proxy({{}}, {{
            get: (target, prop) => {{
                if (prop === 'default') return target;
                if (prop === 'icons') return window.lucide?.icons;
                
                return ({{ size = 24, color = "currentColor", strokeWidth = 2, className = "", ...props }}) => {{
                    // Try to get icon from global Lucide object
                    const iconName = prop; // PascalCase (e.g. LayoutDashboard)
                    const iconNode = window.lucide?.icons?.[iconName];

                    if (iconNode && window.lucide?.createElement) {{
                        try {{
                            const svgEl = window.lucide.createElement(iconNode);
                            
                            // Apply attributes manually since createElement returns a DOM node
                            svgEl.setAttribute('width', size);
                            svgEl.setAttribute('height', size);
                            svgEl.setAttribute('stroke', color);
                            svgEl.setAttribute('stroke-width', strokeWidth);
                            if (className) svgEl.setAttribute('class', className);
                            
                            // Apply other props
                            Object.entries(props).forEach(([key, val]) => {{
                                if (val !== undefined && key !== 'children') {{
                                    // Convert camelCase to kebab-case for attributes if needed, or just set
                                    const attrKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
                                    svgEl.setAttribute(attrKey, val);
                                }}
                            }});

                            return <span dangerouslySetInnerHTML={{{{ __html: svgEl.outerHTML }}}} style={{{{ display: 'inline-flex' }}}} />;
                        }} catch (e) {{
                            console.warn("Lucide rendering failed:", e);
                        }}
                    }}
                    
                    // Fallback
                    return <span style={{{{ width: size, height: size, display: 'inline-block', background: '#ddd' }}}} title={{`Icon ${{iconName}} not found`}} />;
                }}
            }}
        }});

        // Expose to global scope for generated code
        window.Lucide = Lucide;
        const LucideIcons = Lucide; 

        // ------------------------------------------

        // Simple mock for component library

        const ComponentLibrary = {{
           Button: (props) => <button {{...props}} className={{"px-4 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700 " + props.className}}>{{props.children}}</button>,
            Card: (props) => <div {{...props}} className={{"bg-white p-6 rounded-lg shadow-sm border " + props.className}}>{{props.children}}</div>,
            Input: (props) => <input {{...props}} className={{"w-full p-2 border rounded focus:ring-2 ring-blue-500 " + props.className}} />,
            Sidebar: ({{ items, activeItem, position, className, ...props }}) => (
                <aside className={{"bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 w-64 p-4 " + className}} {{...props}}>
                   <div className="space-y-1">
                      {{items?.map((item, idx) => {{
                          const Icon = window.Lucide[item.icon] || window.Lucide.Circle;
                          return (
                              <button key={{idx}} onClick={{item.onClick}} className={{"w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors " + (activeItem === item.label ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400 font-medium' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800')}}>
                                  <Icon size={{18}} />
                                  <span>{{item.label}}</span>
                              </button>
                          );
                      }})}}
                   </div>
                </aside>
            ),
            Navbar: ({{ brand, links, user, className, ...props }}) => (
                <nav className={{"flex items-center justify-between px-6 py-3 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-black/80 backdrop-blur-md " + className}} {{...props}}>
                    <div className="font-bold text-lg tracking-tight">{{brand}}</div>
                    <div className="flex items-center gap-6">
                        {{links?.map(l => <a key={{l.label}} href={{l.href}} className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">{{l.label}}</a>)}}
                        {{user && <img src={{user.avatar}} alt={{user.name}} className="w-8 h-8 rounded-full ring-2 ring-gray-100 dark:ring-gray-800" />}}
                    </div>
                </nav>
            ),
            Table: ({{ headers, data, className, ...props }}) => (
                <div className={{"w-full overflow-auto " + className}} {{...props}}>
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs text-gray-500 uppercase bg-gray-50 dark:bg-gray-900/50">
                            <tr>{{headers?.map((h, i) => <th key={{i}} className="px-6 py-3 font-medium">{{h}}</th>)}}</tr>
                        </thead>
                        <tbody>
                            {{data?.map((row, i) => (
                                <tr key={{i}} className="bg-white dark:bg-black border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors">
                                    {{Object.values(row).map((cell, j) => <td key={{j}} className="px-6 py-4">{{cell}}</td>)}}
                                </tr>
                            ))}}
                        </tbody>
                    </table>
                </div>
            ),
            Chart: ({{ type, color, className, ...props }}) => (
                <div className={{"flex flex-col items-center justify-center p-8 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-dashed border-gray-300 dark:border-gray-700 " + className}} {{...props}}>
                    <window.Lucide.BarChart2 className={{"w-8 h-8 opacity-50 mb-2 " + (color ? "text-" + color + "-500" : "text-gray-400")}} />
                    <span className="text-xs font-mono text-gray-400 uppercase">Mock {{type}} Chart</span>
                </div>
            )
        }};
        const {{ Button, Card, Input, Sidebar, Navbar, Table, Chart }} = ComponentLibrary;

        {clean_code}
        
        // Auto-mount logic
        const candidates = {{
            Component: typeof Component !== 'undefined' ? Component : null,
            Dashboard: typeof Dashboard !== 'undefined' ? Dashboard : null,
            LandingPage: typeof LandingPage !== 'undefined' ? LandingPage : null,
            LoginPage: typeof LoginPage !== 'undefined' ? LoginPage : null,
            ContactForm: typeof ContactForm !== 'undefined' ? ContactForm : null,
            App: typeof App !== 'undefined' ? App : null
        }};
        
        const MountPoint = Object.values(candidates).find(c => c !== null);
                          
        if (MountPoint) {{
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<MountPoint />);
        }} else {{
             // Try to find any function formatted like a component
             document.body.innerHTML = '<div style="padding: 20px; color: red;">Could not auto-detect Main Component. Please check console.</div>';
        }}
    </script>
</body>
</html>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    # Return localhost URL
    return jsonify({"url": f"{FRONTEND_URL}/view/{filename}"})

@app.route('/view/<filename>')
def view_deployment(filename):
    return send_from_directory(DEPLOY_DIR, filename)

if __name__ == '__main__':
    print("Starting Python AI Service on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)
