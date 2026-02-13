const axios = require('axios');

// Configure AI Service URL
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5001';

/**
 * GENERATE UI
 * Calls the Python AI Service to generate UI code based on prompt.
 */
exports.generateUI = async (req, res) => {
  const { prompt } = req.body;
  
  if (!prompt) {
    return res.status(400).json({ error: "Prompt is required" });
  }
  try {
    console.log(`[Node] Calling Python AI Service (Generate) for intent: ${prompt}`);

    // Forward request to Python Microservice
    const response = await axios.post(`${AI_SERVICE_URL}/generate`, {
        prompt
    });
    
    // Return Python's deterministic response to Frontend
    const { code, meta } = response.data;
    
    // Asynchronously log to MongoDB (don't block response)
    const GeneratedUI = require('../models/GeneratedUI');
    try {
        await GeneratedUI.create({
            prompt,
            code,
            intent: meta?.intent || 'unknown'
        });
    } catch (dbErr) {
        console.error("DB Log Error:", dbErr.message);
    }

    res.json(response.data);

  } catch (error) {
    console.error("AI Service Error:", error.message);
    if (error.code === 'ECONNREFUSED') {
         return res.status(503).json({ 
             error: "AI Service Unavailable. Please ensure the Python service is running on port 5001." 
         });
    }
    res.status(500).json({ error: "Generation failed." });
  }
};

/**
 * MODIFY UI
 * Calls Python AI Service to tweak existing code.
 */
exports.modifyUI = async (req, res) => {
  const { prompt, currentCode } = req.body;

  if (!prompt || !currentCode) {
    return res.status(400).json({ error: "Prompt and currentCode are required" });
  }

  try {
    console.log(`[Node] Calling Python AI Service (Modify) for: ${prompt}`);

    const response = await axios.post(`${AI_SERVICE_URL}/modify`, {
      prompt,
      currentCode,
    });

    res.json(response.data);
  } catch (error) {
    console.error("AI Service Error:", error.message);
    res.status(500).json({ error: "Modification failed." });
  }
};

/**
 * SHARE UI
 * Persists a generated UI snapshot and returns a stable public slug.
 * This enables "custom URLs" similar to Vercel v0 / design tools.
 */
exports.shareUI = async (req, res) => {
  const { prompt, code, intent, plan, explanation } = req.body;

  if (!prompt || !code) {
    return res
      .status(400)
      .json({ error: 'Prompt and code are required to create a shareable link.' });
  }

  // Simple, human-friendly slug (not cryptographically secure – fine for demo)
  const base = (intent || 'ui').toString().slice(0, 12).toLowerCase() || 'ui';
  const randomSuffix = Math.random().toString(36).substring(2, 8);
  const slug = `${base}-${randomSuffix}`;

  const publicBase =
    process.env.PUBLIC_SHARE_BASE_URL || process.env.FRONTEND_URL || '';

  const shareUrl = publicBase
    ? `${publicBase.replace(/\/$/, '')}/share/${slug}`
    : `/share/${slug}`;

  // Best-effort persistence: try to save, but don't fail the response if DB is down
  try {
    const GeneratedUI = require('../models/GeneratedUI');
    const doc = await GeneratedUI.create({
      prompt,
      code,
      intent,
      plan,
      explanation,
      slug,
    });

    return res.status(201).json({
      success: true,
      slug,
      shareUrl,
      createdAt: doc.createdAt,
    });
  } catch (err) {
    console.warn('[ShareUI] Skipping DB persistence, returning ephemeral share URL:', err.message);
    return res.status(201).json({
      success: true,
      slug,
      shareUrl,
      createdAt: new Date().toISOString(),
      note: 'Share URL is ephemeral because the database is not available.',
    });
  }
};

/**
 * GET SHARED UI BY SLUG
 * Allows public read-only access to a previously shared UI snapshot.
 */
exports.getSharedUI = async (req, res) => {
  const { slug } = req.params;

  if (!slug) {
    return res.status(400).json({ error: 'Slug is required.' });
  }

  try {
    const GeneratedUI = require('../models/GeneratedUI');

    const doc = await GeneratedUI.findOne({ slug }).lean();
    if (!doc) {
      return res.status(404).json({ error: 'Shared UI not found.' });
    }

    res.json({
      prompt: doc.prompt,
      code: doc.code,
      intent: doc.intent,
      plan: doc.plan,
      explanation: doc.explanation,
      createdAt: doc.createdAt,
      slug: doc.slug,
    });
  } catch (err) {
    console.error('[getSharedUI] Failed to load shared UI', err);
    res.status(500).json({ error: 'Failed to load shared UI.' });
  }
};
/**
 * DEPLOY UI (Persistent)
 * Saves the generated UI to MongoDB and returns a viewable URL.
 */
// ... (deployUI start)
exports.deployUI = async (req, res) => {
  const { code, prompt } = req.body;
  if (!code) return res.status(400).json({ error: "No code provided" });

  try {
      const Deployment = require('../models/Deployment');
      
      // Sanitized Title Generator
      const cleanPrompt = (prompt || 'React App').replace(/[^a-zA-Z0-9 ]/g, '').substring(0, 50);
      const docTitle = cleanPrompt || 'Ryze Deployment';

      // Prepare HTML Template
      const cleanCode = code
          .split('\n')
          .filter(l => !l.trim().startsWith('import '))
          .join('\n')
          .replace('export default function', 'function')
          .replace('export default', '');
      
      // Pre-calculate Base URL for template injection
      const protocol = req.secure ? 'https' : req.protocol;
      const baseUrl = process.env.BASE_URL || `${protocol}://${req.get('host')}`;
      const frontendUrl = process.env.FRONTEND_URL || 'https://ryze-ai-agent.vercel.app';

      const finalHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${docTitle} | Ryze AI</title>
    <meta name="description" content="Generated by Ryze AI: ${cleanPrompt}">
    <meta property="og:title" content="${docTitle} | Ryze AI" />
    <meta property="og:description" content="View this AI-generated UI component live." />
    <meta property="og:image" content="${frontendUrl}/og-image.png" />
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" href="${frontendUrl}/favicon.ico">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { margin: 0; background: #f0f2f5; font-family: sans-serif; }
        .spinner { border: 4px solid rgba(0,0,0,0.1); width: 36px; height: 36px; border-radius: 50%; border-left-color: #3b82f6; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .center-loader { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; color: #6b7280; }
    </style>
</head>
<body>
    <div id="root">
        <div class="center-loader">
            <div class="spinner"></div>
            <p style="margin-top: 16px; font-size: 0.875rem;">Loading generated UI...</p>
        </div>
    </div>
    
    <!-- Scripts -->
    <script>
        function copyLink() {
            navigator.clipboard.writeText(window.location.href);
            const btn = document.getElementById('shareBtn');
            const original = btn.innerHTML;
            btn.innerHTML = 'Copied!';
            btn.style.background = '#e5e7eb';
            setTimeout(() => {
                btn.innerHTML = original;
                btn.style.background = '#ffffff';
            }, 2000);
        }
    </script>
    
    <!-- Validation Toolbar -->
     <div style="position: fixed; bottom: 24px; right: 24px; z-index: 10000; display: flex; align-items: center; gap: 12px; font-family: system-ui, -apple-system, sans-serif;">
        <a id="downloadBtn" href="#" download="ryze-component.html" style="background: #ffffff; color: #000000; text-decoration: none; border: 1px solid #e5e7eb; padding: 8px 16px; border-radius: 9999px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-weight: 500; transition: all 0.2s; display: flex; align-items: center; gap: 6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Download
        </a>
        <button onclick="copyLink()" id="shareBtn" style="background: #ffffff; color: #000000; border: 1px solid #e5e7eb; padding: 8px 16px; border-radius: 9999px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-weight: 500; transition: all 0.2s; display: flex; align-items: center; gap: 6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            Share
        </button>
        <a href="${frontendUrl}" target="_blank" style="text-decoration: none;">
            <div style="background: #000000; color: #ffffff; padding: 8px 16px; border-radius: 9999px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-weight: 600; display: flex; align-items: center; gap: 6px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                Built with Ryze
            </div>
        </a>
    </div>

    <!-- React Implementation -->
    <script type="text/babel">
        // ... (Same React Logic)
        const { useState, useEffect, useRef } = React;
        const Lucide = new Proxy({}, {
            get: (target, prop) => {
                if (prop === 'default') return target;
                if (prop === 'icons') return window.lucide?.icons;
                return ({ size = 24, color = "currentColor", strokeWidth = 2, className = "", ...props }) => {
                    const iconName = prop;
                    const iconNode = window.lucide?.icons?.[iconName];
                    if (iconNode && window.lucide?.createElement) {
                        try {
                            const svgEl = window.lucide.createElement(iconNode);
                            svgEl.setAttribute('width', size);
                            svgEl.setAttribute('height', size);
                            svgEl.setAttribute('stroke', color);
                            svgEl.setAttribute('stroke-width', strokeWidth);
                            if (className) svgEl.setAttribute('class', className);
                            Object.entries(props).forEach(([key, val]) => {
                                if (val !== undefined && key !== 'children') {
                                    const attrKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
                                    svgEl.setAttribute(attrKey, val);
                                }
                            });
                            return <span dangerouslySetInnerHTML={{ __html: svgEl.outerHTML }} style={{ display: 'inline-flex' }} />;
                        } catch (e) {
                            console.warn("Lucide rendering failed:", e);
                        }
                    }
                    return <span style={{ width: size, height: size, display: 'inline-block', background: '#ddd' }} title={\`Icon \${iconName} not found\`} />;
                }
            }
        });
        window.Lucide = Lucide;
        const LucideIcons = Lucide;
        
         const ComponentLibrary = {
            Button: (props) => <button {...props} className={"px-4 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700 " + props.className}>{props.children}</button>,
            Card: (props) => <div {...props} className={"bg-white p-6 rounded-lg shadow-sm border " + props.className}>{props.children}</div>,
            Input: (props) => <input {...props} className={"w-full p-2 border rounded focus:ring-2 ring-blue-500 " + props.className} />,
            Sidebar: ({ items, activeItem, position, className, ...props }) => (
                <aside className={"bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 w-64 p-4 " + className} {...props}>
                   <div className="space-y-1">
                      {items?.map((item, idx) => {
                          const Icon = window.Lucide[item.icon] || window.Lucide.Circle;
                          return (
                              <button key={idx} onClick={item.onClick} className={"w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors " + (activeItem === item.label ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400 font-medium' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800')}>
                                  <Icon size={18} />
                                  <span>{item.label}</span>
                              </button>
                          );
                      })}
                   </div>
                </aside>
            ),
            Navbar: ({ brand, links, user, className, ...props }) => (
                <nav className={"flex items-center justify-between px-6 py-3 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-black/80 backdrop-blur-md " + className} {...props}>
                    <div className="font-bold text-lg tracking-tight">{brand}</div>
                    <div className="flex items-center gap-6">
                        {links?.map(l => <a key={l.label} href={l.href} className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">{l.label}</a>)}
                        {user && <img src={user.avatar} alt={user.name} className="w-8 h-8 rounded-full ring-2 ring-gray-100 dark:ring-gray-800" />}
                    </div>
                </nav>
            ),
            Table: ({ headers, data, className, ...props }) => (
                <div className={"w-full overflow-auto " + className} {...props}>
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs text-gray-500 uppercase bg-gray-50 dark:bg-gray-900/50">
                            <tr>{headers?.map((h, i) => <th key={i} className="px-6 py-3 font-medium">{h}</th>)}</tr>
                        </thead>
                        <tbody>
                            {data?.map((row, i) => (
                                <tr key={i} className="bg-white dark:bg-black border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors">
                                    {Object.values(row).map((cell, j) => <td key={j} className="px-6 py-4">{cell}</td>)}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ),
            Chart: ({ type, color, className, ...props }) => (
                <div className={"flex flex-col items-center justify-center p-8 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-dashed border-gray-300 dark:border-gray-700 " + className} {...props}>
                    <window.Lucide.BarChart2 className={"w-8 h-8 opacity-50 mb-2 " + (color ? "text-" + color + "-500" : "text-gray-400")} />
                    <span className="text-xs font-mono text-gray-400 uppercase">Mock {type} Chart</span>
                </div>
            )
        };
        const { Button, Card, Input, Sidebar, Navbar, Table, Chart } = ComponentLibrary;

        ${cleanCode}
        
        const candidates = {
            Component: typeof Component !== 'undefined' ? Component : null,
            Dashboard: typeof Dashboard !== 'undefined' ? Dashboard : null,
            LandingPage: typeof LandingPage !== 'undefined' ? LandingPage : null,
            LoginPage: typeof LoginPage !== 'undefined' ? LoginPage : null,
            App: typeof App !== 'undefined' ? App : null
        };
        const MountPoint = Object.values(candidates).find(c => c !== null);
        if (MountPoint) {
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<MountPoint />);
            
            // Hydrate Download Link with Deployment ID
            const deployId = window.location.pathname.split('/').pop();
            const dlBtn = document.getElementById('downloadBtn');
            if(dlBtn) dlBtn.href = '/download/' + deployId;
            
        } else {
             document.body.innerHTML = '<div style="padding: 20px; color: red;">Could not auto-detect Main Component. Please check console.</div>';
        }
    </script>
</body>
</html>`;

      const doc = await Deployment.create({
          _id: new (require('mongoose').Types.ObjectId)(), 
          originalCode: code,
          htmlContent: finalHtml,
          prompt: cleanPrompt,
          title: docTitle
      });
      
      const deploymentUrl = `${baseUrl}/view/${doc._id}`;
      res.json({ url: deploymentUrl });

  } catch (err) {
      console.error("Deploy Error:", err);
      res.status(500).json({ error: "Deployment failed" });
  }
};

exports.viewDeployment = async (req, res) => {
    try {
        const Deployment = require('../models/Deployment');
        const doc = await Deployment.findById(req.params.id);
        if (!doc) return res.status(404).send('Deployment not found');
        res.setHeader('Content-Type', 'text/html');
        res.send(doc.htmlContent);
    } catch (err) {
        res.status(500).send('Error loading deployment');
    }
};

exports.downloadDeployment = async (req, res) => {
    try {
        const Deployment = require('../models/Deployment');
        const doc = await Deployment.findById(req.params.id);
        if (!doc) return res.status(404).send('Deployment not found');
        
        res.setHeader('Content-Type', 'text/html');
        res.setHeader('Content-Disposition', `attachment; filename="ryze-${doc._id}.html"`);
        res.send(doc.htmlContent);
    } catch (err) {
        res.status(500).send('Error downloading deployment');
    }
};
