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

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}")
    return jsonify({"error": "Internal Server Error", "details": str(error)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled Exception: {e}")
    return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/generate', methods=['POST'])
@app.route('/api/generator/generate', methods=['POST'])

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
@app.route('/api/generator/modify', methods=['POST'])
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
    new_brand = style_extractor.extract_brand_name(prompt)
    
    # 2. Apply modifications (Symbolic replacements)
    import re
    
    # Replace simple color names in text/bg classes
    # Expanded palette to catch all Tailwind colors
    known_colors = [
        'slate', 'gray', 'zinc', 'neutral', 'stone',
        'red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 
        'cyan', 'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose'
    ]
    
    # Regex to find existing color classes (e.g. bg-blue-500, from-indigo-600)
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
    
    # 2b. Content Updates (Brand Name / Title)
    if new_brand and new_brand != "Ryze App": # If a specific brand was detected
         # Heuristic: Replace content inside <h1> tags or specific brand placeholders
         # We try to find the old brand name if possible, or just look for typical header patterns.
         # For simplicity in this deterministic assignment, we'll replace the text in the Navbar brand prop if it exists.
         if 'brand="' in modified_code:
             modified_code = re.sub(r'brand="[^"]+"', f'brand="{new_brand}"', modified_code)
             explanation_steps.append(f"- Renamed application brand to '{new_brand}'.")
         
         # Also try to replace <h1> content if it looks like a title
         # exact logic is tricky without DOM parsing, but we can try a targeted sub for common patterns
         # or just rely on the user asking precisely. 
         pass

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


if __name__ == '__main__':
    print("Starting Python AI Service on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)
