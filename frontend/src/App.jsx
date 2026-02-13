import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
   Send, RefreshCw, ChevronLeft, ChevronRight, Code, Eye, 
   Bot,
   Loader2, Globe, Laptop, Moon, Sun, MonitorPlay, History,
   ShoppingBag, Layout, Users
} from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import * as ComponentLibrary from './components/ui';
import { transform } from '@babel/standalone';

// API Configuration
// -----------------------------------------------------------------------------
// API Configuration
// -----------------------------------------------------------------------------

// Determine Backend Base URL
// In Dev: Defaults to localhost:5000
// In Prod: Uses VITE_API_URL from Vercel Env (must be the root URL or /api/generator specific)
const getBaseUrl = () => {
  if (import.meta.env.DEV) return 'http://localhost:5000';
  
  // Clean up the env var: remove trailing slashes and specific paths to get the root
  // Expecting VITE_API_URL to be like: https://backend.onrender.com/api/generator or just https://backend.onrender.com
  let url = import.meta.env.VITE_API_URL || '';
  url = url.replace(/\/api\/generator\/?$/, ''); // Remove /api/generator if present
  url = url.replace(/\/+$/, ''); // Remove trailing slash
  return url;
};

const BASE_URL = getBaseUrl();

// Derived Endpoints
const API_URL = `${BASE_URL}/api/generator`; // Used for /generate and /modify
const DEPLOY_URL = `${BASE_URL}/deploy`;     // Used for /deploy

// Debug Logs (Verify connectivity logic)
console.log(`[Config] Env: ${import.meta.env.MODE}`);
console.log(`[Config] Base URL: ${BASE_URL}`);
console.log(`[Config] API URL: ${API_URL}`);
console.log(`[Config] Deploy URL: ${DEPLOY_URL}`);


// -----------------------------------------------------------------------------
// Preview Component
// -----------------------------------------------------------------------------
const Preview = ({ code, error, isFullScreen, setIsFullScreen, handleCopyCode, handleDownloadCode, handleDeploy }) => {
  const [Component, setComponent] = useState(null);
  const [runtimeError, setRuntimeError] = useState(null);
  const [viewMode, setViewMode] = useState('desktop'); // 'desktop', 'tablet', 'mobile'

  useEffect(() => {
    if (!code) return;
    
    try {
      // 1. Transpile JSX/ES6 to ES5
      const transformedCode = transform(code, {
        presets: ['react', 'env'],
        filename: 'preview.jsx',
      }).code;

      // 2. Prepare execution scope
      // We expose React and our Component Library to the evaluated code
      const scope = { 
        React, 
        ...React, // Expose useState, useEffect etc directly if needed
        ...ComponentLibrary,
        ...LucideIcons, // Expose Lucide icons directly if needed in scope
        Lucide: LucideIcons // Expose Lucide namespace object
      };
      
      // 3. Wrap code to handle exports
      let executableCode = transformedCode;
      if (executableCode.includes('exports.default =')) {
         executableCode += '; return exports.default;';
      } else if (executableCode.includes('export default')) {
         executableCode = executableCode.replace('export default', 'return');
      } else {
         // Fallback
      }

      // 4. Execute
      const scopeKeys = Object.keys(scope);
      const scopeValues = Object.values(scope);
      
      const func = new Function('require', 'exports', ...scopeKeys, executableCode);
      
      const mockRequire = (mod) => {
        if (mod === 'react') return React;
        if (mod === 'lucide-react') return LucideIcons;
        return {}; 
      };
      const mockExports = {};

      const Result = func(mockRequire, mockExports, ...scopeValues);
      
      const FinalComponent = Result || mockExports.default;

      if (FinalComponent) {
        setComponent(() => FinalComponent);
        setRuntimeError(null);
      } else {
        throw new Error("No default export found in generated code.");
      }
    } catch (err) {
      console.error("Preview Error:", err);
      setRuntimeError(err.toString());
    }
  }, [code]);

  if (error || runtimeError) {
    return (
      <div className="flex h-full flex-col items-center justify-center p-8 text-red-500 bg-red-50 dark:bg-red-900/10 rounded-lg border border-red-200 dark:border-red-900">
        <MonitorPlay className="h-12 w-12 mb-4 opacity-50" />
        <h3 className="text-lg font-semibold mb-2">Rendering Error</h3>
        <pre className="text-sm bg-white/50 dark:bg-black/20 p-4 rounded max-w-full overflow-auto whitespace-pre-wrap">
          {error || runtimeError}
        </pre>
      </div>
    );
  }

  if (!Component) {
    return (
      <div className="flex h-full items-center justify-center text-gray-400">
        <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-2" />
            <p>Compiling Preview...</p>
        </div>
      </div>
    );
  }

  // Width mapping
  const widthMap = {
      desktop: '100%',
      tablet: '768px',
      mobile: '375px'
  };


  const containerClasses = isFullScreen 
    ? "fixed inset-0 z-[100] bg-gray-100 dark:bg-gray-900 flex flex-col" 
    : "w-full h-full flex flex-col bg-gray-50/50 dark:bg-gray-900/30 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-800";

  return (
    <div className={containerClasses}>
       {/* Preview Toolbar */}
       <div className="flex items-center justify-between px-4 py-2 bg-white dark:bg-black border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
             <button 
                onClick={() => setViewMode('desktop')} 
                className={`p-1.5 rounded-md transition-all ${viewMode === 'desktop' ? 'bg-white dark:bg-gray-700 shadow-sm text-blue-500' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
                title="Desktop View"
             >
                <LucideIcons.Monitor className="w-4 h-4" />
             </button>
             <button 
                onClick={() => setViewMode('tablet')} 
                className={`p-1.5 rounded-md transition-all ${viewMode === 'tablet' ? 'bg-white dark:bg-gray-700 shadow-sm text-blue-500' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
                title="Tablet View"
             >
                <LucideIcons.Tablet className="w-4 h-4" />
             </button>
             <button 
                onClick={() => setViewMode('mobile')} 
                className={`p-1.5 rounded-md transition-all ${viewMode === 'mobile' ? 'bg-white dark:bg-gray-700 shadow-sm text-blue-500' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
                title="Mobile View"
             >
                <LucideIcons.Smartphone className="w-4 h-4" />
             </button>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Export Actions */}
                <button 
                    onClick={handleDeploy}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors text-xs font-semibold shadow-sm"
                    title="Deploy to Edge"
                >
                    <LucideIcons.Rocket className="w-3.5 h-3.5" /> Deploy
                </button>
                <div className="w-px h-4 bg-gray-200 dark:bg-gray-800 mx-1"></div>
                <button 
                     onClick={() => window.open('mailto:feedback@ryze.ai?subject=Ryze%20Feedback', '_blank')}
                     className="p-1.5 rounded-md text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                     title="Send Feedback"
                >
                    <LucideIcons.MessageSquare className="w-4 h-4" />
                </button>
                <button 
                    onClick={handleCopyCode}
                    className="p-1.5 rounded-md text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    title="Copy Code"
                >
                    <LucideIcons.Copy className="w-4 h-4" />
                </button>
                <button 
                    onClick={handleDownloadCode}
                    className="p-1.5 rounded-md text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    title="Download .jsx"
                >
                    <LucideIcons.Download className="w-4 h-4" />
                </button>
            </div>

             <button 
                onClick={() => setIsFullScreen(!isFullScreen)}
                className="flex items-center gap-2 text-xs font-medium text-gray-500 hover:text-blue-600 transition-colors"
             >
                {isFullScreen ? <LucideIcons.Minimize2 className="w-4 h-4" /> : <LucideIcons.Maximize2 className="w-4 h-4" />}
                {isFullScreen ? 'Exit Full Screen' : 'Full Screen'}
             </button>
          </div>
      

       {/* Render Area */}
       <div className="flex-1 overflow-auto flex justify-center bg-gray-50/50 dark:bg-[#0c0c0c] relative p-4" style={{ backgroundImage: 'radial-gradient(#e5e7eb 1px, transparent 1px)', backgroundSize: '20px 20px' }}>
          <div 
             className="bg-white dark:bg-background shadow-2xl transition-all duration-500 ease-in-out border border-gray-200 dark:border-gray-800 overflow-hidden relative"
             style={{ 
                 width: widthMap[viewMode], 
                 height: viewMode === 'mobile' ? '667px' : (viewMode === 'tablet' ? '1024px' : '100%'),
                 borderRadius: viewMode === 'desktop' ? '0.5rem' : '1.5rem',
                 maxHeight: isFullScreen ? '100%' : undefined
             }}
          >
             <div className="w-full h-full overflow-auto scrollbar-hide">
                {Component && <Component />}
             </div>
          </div>
       </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// App Component
// -----------------------------------------------------------------------------
export default function App() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]); // Array of { prompt, code, plan, explanation, timestamp }
  const [currentStep, setCurrentStep] = useState(-1); // Pointer to current history item
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(''); // 'Thinking...', 'Generating...', etc.
  
  // --- Chat History & Persistence ---
  const [chats, setChats] = useState(() => {
    if (typeof window !== 'undefined') {
       const saved = localStorage.getItem('ryze_chats');
       return saved ? JSON.parse(saved) : [];
    }
    return [];
  });
  const [currentChatId, setCurrentChatId] = useState(null);

  // Helper to save current state to history
  const saveToHistory = (newHistory, newStep) => {
      let chatId = currentChatId;
      let newChats = [...chats];
      
      if (!chatId) {
          // New Chat Creation
          chatId = Date.now().toString();
          setCurrentChatId(chatId);
          // Derive Title
          const firstPrompt = newHistory.find(m => m.role === 'user')?.content || "New Project";
          const title = firstPrompt.length > 25 ? firstPrompt.slice(0, 25) + '...' : firstPrompt;
          
          newChats.unshift({
              id: chatId,
              title,
              history: newHistory,
              currentStep: newStep,
              updatedAt: Date.now()
          });
      } else {
          // Update Existing
          const index = newChats.findIndex(c => c.id === chatId);
          if (index !== -1) {
             newChats[index] = {
                 ...newChats[index],
                 history: newHistory,
                 currentStep: newStep,
                 updatedAt: Date.now()
             };
             // Move to top
             const updatedChat = newChats.splice(index, 1)[0];
             newChats.unshift(updatedChat);
          }
      }
      setChats(newChats);
      localStorage.setItem('ryze_chats', JSON.stringify(newChats));
  };

  const startNewChat = () => {
      setCurrentChatId(null);
      setHistory([]);
      setCurrentStep(-1);
      setInput('');
      // Optional: Clear code preview?
  };

  const selectChat = (chatId) => {
      const chat = chats.find(c => c.id === chatId);
      if (chat) {
          setCurrentChatId(chatId);
          setHistory(chat.history);
          setCurrentStep(chat.currentStep);
          // activeTab logic handled by user interaction
      }
  };
  
  const [activeTab, setActiveTab] = useState('preview'); // 'preview' | 'code' | 'plan'
  const [darkMode, setDarkMode] = useState(() => {
    // Check local storage or system preference
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('ryze-theme');
      if (saved) return saved === 'dark';
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return true;
  });
  
  // Full Screen State
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  // Resizable Panels State
  const [sidebarWidth, setSidebarWidth] = useState(288); // History Sidebar
  const [chatPanelWidth, setChatPanelWidth] = useState(400); // Chat Interface
  
  const resizingTarget = useRef(null); // 'sidebar' or 'chat'

  // Global Resizing Logic
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!resizingTarget.current) return;
      
      if (resizingTarget.current === 'sidebar') {
          // Clamp History Sidebar (200px - 500px)
          const newWidth = Math.max(200, Math.min(500, e.clientX));
          setSidebarWidth(newWidth);
      } else if (resizingTarget.current === 'chat') {
          // Clamp Chat Panel (300px - 800px)
          // Width is relative to start of chat panel. 
          // Chat panel starts after sidebar (if open)
          const startX = isSidebarOpen ? sidebarWidth : 0;
          const newWidth = Math.max(300, Math.min(800, e.clientX - startX));
          setChatPanelWidth(newWidth);
      }
    };

    const handleMouseUp = () => {
      resizingTarget.current = null;
      document.body.style.cursor = 'default';
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isSidebarOpen, sidebarWidth]); // Dependency needed for calculation

  const startResizingSidebar = (e) => {
    resizingTarget.current = 'sidebar';
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  };

  const startResizingChat = (e) => {
    resizingTarget.current = 'chat';
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  };

  // Splash Screen State
  const [showSplash, setShowSplash] = useState(true);
  const [splashStatus, setSplashStatus] = useState('Initializing Ryze AI Agent...');
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history, loading]);

  useEffect(() => {
    const timers = [
        setTimeout(() => setSplashStatus('Connecting to Global Edge Nodes...'), 800),
        setTimeout(() => setSplashStatus('Loading v2.0 Tensor Cores...'), 1600),
        setTimeout(() => setSplashStatus('System Optimization Complete.'), 2200),
        setTimeout(() => setShowSplash(false), 2800)
    ];
    return () => timers.forEach(clearTimeout);
  }, []);
  
  // Keyboard Shortcuts
  useEffect(() => {
       const handleKeyDown = (e) => {
           // Full Screen Toggle
           if (e.key === 'Escape' && isFullScreen) {
               setIsFullScreen(false);
           }
           // Focus Input (Cmd+K)
           if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
               e.preventDefault();
               document.querySelector('textarea')?.focus();
           }
           // Undo (Cmd+Z)
           if ((e.metaKey || e.ctrlKey) && e.key === 'z') {
               e.preventDefault();
               if (currentStep > 0) setCurrentStep(s => Math.max(-1, s - 2));
           }
       };
       window.addEventListener('keydown', handleKeyDown);
       return () => window.removeEventListener('keydown', handleKeyDown);
   }, [isFullScreen, currentStep]);

  // Export Functions
  const handleCopyCode = async () => {
    if (!currentCode) return;
    try {
      await navigator.clipboard.writeText(currentCode);
      setStatus('Copied to clipboard!');
      setTimeout(() => setStatus(''), 2000);
    } catch (err) {
      console.error('Failed to copy class', err);
    }
  };

  const handleDownloadCode = () => {
    if (!currentCode) return;
    const blob = new Blob([currentCode], { type: 'text/javascript' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Ryze_Component_v${currentStep > -1 ? Math.floor(currentStep / 2) + 1 : 1}.jsx`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setStatus('Downloaded file!');
    setTimeout(() => setStatus(''), 2000);
  };


  const handleGithubExport = () => {
      window.open('https://github.com/new', '_blank');
      navigator.clipboard.writeText(currentCode);
      setStatus('✅ GitHub opened (Code copied, paste it there!)');
      setTimeout(() => setStatus(''), 4000);
  };

  // Deploy to Edge (Real Backend)
  const handleDeploy = async () => {
      setLoading(true);
      setStatus('🚀 initializing_pipeline...');
      
      try {
          await new Promise(r => setTimeout(r, 600));
          setStatus('📦 bundling_assets...');
          
          const deployPrompt = currentItem?.prompt || history.find(m => m.role === 'user')?.content || 'React Component';
          const res = await axios.post(DEPLOY_URL, { 
              code: currentCode,
              prompt: deployPrompt
          });
          const liveUrl = res.data.url;
          
          await new Promise(r => setTimeout(r, 800));
          setStatus(`✅ Live at: ${liveUrl}`);
          setLoading(false);
          
          await navigator.clipboard.writeText(liveUrl);
          if (confirm(`Deployment Successful!\n\nLive URL: ${liveUrl}\n\n(Copied to clipboard). Open now?`)) {
              window.open(liveUrl, '_blank');
          }
          setTimeout(() => setStatus(''), 5000);
          
      } catch (err) {
          console.error("Deployment Failed:", err);
          setStatus('⚠️ Deployment failed. Please try again.');
          alert(`Deployment Failed: ${err.response?.data?.error || err.message}`);
          setTimeout(() => setStatus(''), 5000);
      }
  };

  // Dynamic Title
  useEffect(() => {
      if (history.length > 0 && currentStep >= 0) {
          const lastPrompt = history[currentStep].prompt;
          // specific logic to update title based on prompt
             if (lastPrompt) {
                 const title = lastPrompt.split(' ').slice(0, 3).join(' ') + '...';
                 document.title = `${title} | Ryze AI`;
             }
         
      } else {
          document.title = 'Ryze AI - Neural UI Generator';
      }
  }, [history, currentStep]);

  // Apply dark mode & persist
  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
      localStorage.setItem('ryze-theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('ryze-theme', 'light');
    }
  }, [darkMode]);




  // Initial Welcome Status
  useEffect(() => {
     setStatus('Ryze Neural Engine Ready');
     setTimeout(() => setStatus(''), 3000);
     
     // Check Backend Connectivity
     fetch(`${BASE_URL}/health`)
       .then(res => res.json())
       .then(data => console.log('✅ Backend Connected:', data))
       .catch(err => {
         console.error('❌ Backend Connection Failed:', err);
         setStatus('⚠️ Backend not reachable. Ensure server is running on port 5000.');
       });
  }, []);

  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Voice input is not supported in this browser.');
      return;
    }
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();
    setStatus('🎤 Listening...');
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(prev => prev + ' ' + transcript);
      setStatus('');
    };
    
    recognition.onerror = (event) => {
      console.error(event.error);
      setStatus('');
    };
    recognition.onend = () => setStatus('');
  };

  const handleGenerate = async (overridePrompt = null) => {
    const promptToUse = overridePrompt || input;
    if (!promptToUse.trim()) return;
    
    setLoading(true);
    setStatus('Planning UI structure...');
    
    // Add temporary user message
    const newMessage = { 
        role: 'user', 
        content: promptToUse, 
        timestamp: new Date().toISOString() 
    };

    try {
      let response;
      
      // Simulate "Thinking" steps for advanced AI feel
      setStatus('🧠 Analyzing Intent...');
      await new Promise(r => setTimeout(r, 600));
      
      setStatus('🔍 Extracting Entities...');
      await new Promise(r => setTimeout(r, 500));
      
      setStatus('🎨 selecting_template.py...');
      await new Promise(r => setTimeout(r, 500));

      if (currentStep >= 0 && history[currentStep].code) {
         setStatus('⚡ Iterating on design...');
         response = await axios.post(`${API_URL}/modify`, {
             prompt: promptToUse,
             currentCode: history[currentStep].code
         }, {
            timeout: 300000 // 5 minutes
         });
      } else {
         setStatus('⚛️ Compiling React Component...');
         
         // Free Tier Cold Start Notification
         const coldStartTimer = setTimeout(() => {
             setStatus('⏳ Waking up AI Agent (Free Tier Cold Start)... please wait up to 60s');
         }, 8000);

         response = await axios.post(`${API_URL}/generate`, {
             prompt: promptToUse
         }, {
            timeout: 300000 // 5 minutes
         });
         
         clearTimeout(coldStartTimer);
      }

      const { plan, code, explanation } = response.data;
      
      const newHistoryItem = {
          role: 'assistant',
          prompt: input,
          plan,
          code,
          explanation,
          timestamp: new Date().toISOString()
      };

      const updatedHistory = [...history.slice(0, currentStep + 1), newMessage, newHistoryItem];
      setHistory(updatedHistory);
      const newStep = currentStep + 2; 
      
      // Auto-Save Code
      saveToHistory(updatedHistory, newStep);
      
      setCurrentStep(prev => prev + 2); // Advance past user msg + ai response
      setInput('');
      setActiveTab('preview');
    } catch (error) {
       console.error("Generation failed", error);
       setStatus('Error generated. Please try again.');
       // Handle error state properly in production
    } finally {
      setLoading(false);
      setStatus('');
    }
  };

  const handleCodeEdit = (newCode) => {
      // Create a fork in history when code is manually edited?
      // For simplicity, just update current step's code but typically immutable history is better.
      // Let's implement an immutable update:
      if (currentStep < 0) return;

      const currentItem = history[currentStep];
      if (currentItem.role !== 'assistant') return;

      const newItem = { 
          ...currentItem, 
          code: newCode, 
          explanation: "Manual Edit" 
      };

      setHistory(prev => [...prev.slice(0, currentStep), newItem]);
  };

  const currentItem = currentStep >= 0 ? history[currentStep] : null;
  const currentCode = currentItem?.code || '';
  const currentPlan = currentItem?.plan || '';
  const currentExplanation = currentItem?.explanation || '';

  if (showSplash) {
    return (
        <div className="flex h-screen w-full items-center justify-center bg-gray-50 dark:bg-black font-sans animate-out fade-out duration-500 fill-mode-forwards">
             <div className="flex flex-col items-center gap-6 animate-pulse">
                <div className="relative w-24 h-24 flex items-center justify-center">
                    <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-[40px] animate-pulse"></div>
                    <div className="absolute inset-0 border border-blue-500/30 rounded-full animate-[spin_3s_linear_infinite]"></div>
                    <div className="absolute inset-2 border border-purple-500/30 rounded-full animate-[spin_5s_linear_infinite_reverse]"></div>
                    <div className="relative bg-black p-4 rounded-full ring-1 ring-white/10">
                        <Laptop className="h-8 w-8 text-blue-500" />
                    </div>
                </div>
                <div className="text-center space-y-2">
                    <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">Ryze AI</h2>
                    <p className="text-xs text-blue-500 font-mono tracking-widest uppercase animate-pulse">{splashStatus}</p>
                </div>
             </div>
        </div>
    );
  }

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50 dark:bg-black text-gray-900 dark:text-gray-100 overflow-hidden font-sans relative selection:bg-blue-500/30">
        {/* Advanced Mesh Background */}
        <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
             <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-purple-500/20 rounded-full blur-[120px] animate-[pulse_8s_ease-in-out_infinite]"></div>
             <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-blue-500/20 rounded-full blur-[120px] animate-[pulse_10s_ease-in-out_infinite_reverse]"></div>
        </div>

      {/* Header with Glassmorphism */}
      <header className="sticky top-0 z-50 flex h-16 items-center justify-between border-b border-gray-200/50 dark:border-gray-800/50 bg-white/80 dark:bg-black/80 backdrop-blur-xl px-6 transition-all shadow-sm relative z-10">
        <div className="flex items-center gap-3">
           <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white transition-colors"
              title={isSidebarOpen ? "Close Sidebar" : "Open Sidebar"}
           >
              <Users className="w-5 h-5" />
           </button>
           <div className="bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-xl p-2 shadow-lg shadow-blue-500/20">
              <Laptop className="h-5 w-5 text-white" />
           </div>
           <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">Ryze AI</span>
              <span className="text-[10px] uppercase tracking-widest text-gray-500 font-semibold">Neural UI Generator</span>
           </div>
           
           {/* Status Indicator */}
           <div className="hidden md:flex items-center gap-2 ml-4 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
               <span className="text-[10px] font-medium text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">AI Agent Active</span>
            </div>
        </div>
        <div className="flex items-center gap-4">
           <button 
             onClick={() => setDarkMode(!darkMode)}
             className="relative group p-2.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-all border border-transparent hover:border-gray-200 dark:hover:border-gray-700 active:scale-95 duration-200"
             aria-label="Toggle Theme"
             title={`Switch to ${darkMode ? 'Light' : 'Dark'} Mode`}
           >
             <div className="relative w-5 h-5 flex items-center justify-center">
                <Sun className={`absolute inset-0 h-5 w-5 text-amber-500 transition-all duration-500 ease-in-out ${darkMode ? 'rotate-90 scale-0 opacity-0' : 'rotate-0 scale-100 opacity-100'}`} style={{ transformOrigin: 'center' }} />
                <Moon className={`absolute inset-0 h-5 w-5 text-indigo-500 transition-all duration-500 ease-in-out ${darkMode ? 'rotate-0 scale-100 opacity-100' : '-rotate-90 scale-0 opacity-0'}`} style={{ transformOrigin: 'center' }} />
             </div>
             {/* Tooltip */}
             <span className="absolute top-full mt-2 left-1/2 -translate-x-1/2 px-2 py-1 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 text-[10px] rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                {darkMode ? 'Light Mode' : 'Dark Mode'}
             </span>
           </button>
           <div className="flex items-center gap-1 bg-gray-100/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-lg p-1 border border-gray-200/50 dark:border-gray-800/50">
             <button 
                onClick={() => setCurrentStep(Math.max(-1, currentStep - 2))} // Skip back over (Assistant + User)
                disabled={currentStep <= 0}
                className="p-1.5 hover:bg-white dark:hover:bg-black rounded-md shadow-sm disabled:opacity-30 disabled:shadow-none transition-all"
                title="Undo"
             >
                <ChevronLeft className="h-4 w-4" />
             </button>
             <span className="text-xs font-mono w-8 text-center opacity-50">
                v{currentStep > -1 ? Math.floor(currentStep / 2) + 1 : 0}
             </span>
             <button 
                onClick={() => setCurrentStep(Math.min(history.length - 1, currentStep + 2))}
                disabled={currentStep >= history.length - 1}
                className="p-1.5 hover:bg-white dark:hover:bg-black rounded-md shadow-sm disabled:opacity-30 disabled:shadow-none transition-all"
                title="Redo"
             >
                <ChevronRight className="h-4 w-4" />
             </button>
           </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-1 overflow-hidden relative">
        {/* Background Gradients & Grid */}
        <div className="absolute inset-0 overflow-hidden -z-10 transition-colors duration-500">
            {/* Animated Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
            
            {/* Glowing Orbs */}
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-500/10 rounded-full blur-[120px] animate-pulse"></div>
            <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-500/10 rounded-full blur-[120px] animate-pulse delay-1000"></div>
        </div>
        
        {/* Chat History Sidebar */}
        <aside 
            className={`${isSidebarOpen ? 'flex' : 'hidden'} flex-col bg-gray-900 border-r border-gray-800 text-gray-300 z-20 shrink-0 relative`}
            style={{ width: sidebarWidth }}
        >
             {/* Resizer Handle (Sidebar) */}
             <div 
                onMouseDown={startResizingSidebar}
                className="absolute top-0 right-0 w-1.5 h-full cursor-col-resize hover:bg-blue-500 transition-colors z-50 opacity-0 hover:opacity-100"
                title="Resize Sidebar"
             ></div>

             <div className="p-4">
                 <button 
                    onClick={startNewChat} 
                    className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg transition-all font-medium text-sm shadow-lg shadow-blue-900/20 group"
                 >
                     <LucideIcons.Plus className="w-4 h-4 group-hover:rotate-90 transition-transform" /> 
                     <span>New Project</span>
                 </button>
             </div>
             
             <div className="flex-1 overflow-y-auto px-3 space-y-1 scrollbar-hide py-2">
                 <div className="px-2 py-1.5 text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">Recent Projects</div>
                 {chats.map(chat => (
                     <button 
                        key={chat.id} 
                        onClick={() => selectChat(chat.id)}
                        className={`w-full text-left px-3 py-2.5 rounded-lg text-sm truncate transition-all flex items-center gap-3 group relative ${currentChatId === chat.id ? 'bg-gray-800 text-white shadow-sm' : 'hover:bg-gray-800/40 text-gray-400'}`}
                     >
                        <LucideIcons.MessageSquare className={`w-3.5 h-3.5 flex-shrink-0 ${currentChatId === chat.id ? 'text-blue-500' : 'text-gray-600 group-hover:text-gray-400'}`} />
                        <span className="truncate">{chat.title}</span>
                        {currentChatId === chat.id && <div className="absolute right-2 w-1.5 h-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div>}
                     </button>
                 ))}
                 {chats.length === 0 && (
                     <div className="text-center py-8 text-xs text-gray-600 italic">No history yet</div>
                 )}
             </div>
             
             {/* Simple User Footer */}
             <div className="p-4 border-t border-gray-800 bg-black/20">
                 <div className="flex items-center gap-3 px-1">
                     <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-500 to-blue-500 border border-white/10 flex items-center justify-center text-xs font-bold text-white shadow-inner">
                        AI
                     </div>
                     <div className="flex flex-col">
                         <span className="text-sm font-medium text-white group-hover:text-blue-400 transition-colors">Ryze Admin</span>
                         <span className="text-[10px] text-gray-500">Pro License Active</span>
                     </div>
                 </div>
             </div>
        </aside>

        {/* Left Panel: Chat & Intent (Resizable) */}
        <section 
            className="flex flex-col border-r border-gray-200/50 dark:border-gray-800/50 bg-white/50 dark:bg-black/50 backdrop-blur-md relative"
            style={{ width: chatPanelWidth }}
        >
           {/* Resizer Handle (Chat Panel) */}
           <div 
              onMouseDown={startResizingChat}
              className="absolute top-0 right-0 w-1.5 h-full cursor-col-resize hover:bg-purple-500 transition-colors z-50 opacity-0 hover:opacity-100"
              title="Resize Chat Panel"
           ></div>

           <div className="flex-1 overflow-y-auto p-4 space-y-6">
              {history.length === 0 && (
                  <div className="flex flex-col items-center justify-center h-full text-center space-y-8 p-8 animate-in fade-in duration-700">
                      
                      {/* Neural Visualization Hero */}
                      <div className="relative w-40 h-40 flex items-center justify-center group cursor-pointer mb-6">
                          {/* Conic Gradient Core */}
                          <div className="absolute inset-0 rounded-full bg-[conic-gradient(from_0deg,transparent_0_340deg,white_360deg)] opacity-20 animate-[spin_4s_linear_infinite]"></div>
                          <div className="absolute inset-2 rounded-full bg-black z-10"></div>
                          
                          {/* Inner Glow / Pulse */}
                          <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-[50px] animate-pulse"></div>
                          <div className="absolute inset-0 border border-blue-500/30 rounded-full animate-[spin_10s_linear_infinite]"></div>
                          <div className="absolute inset-4 border border-purple-500/30 rounded-full animate-[spin_15s_linear_infinite_reverse]"></div>
                          
                          {/* Center Icon */}
                          <div className="relative z-20 bg-gradient-to-br from-gray-900 to-black p-6 rounded-full ring-1 ring-white/10 shadow-2xl shadow-blue-500/20 group-hover:scale-105 transition-transform duration-500">
                             <Globe className="h-12 w-12 text-blue-400 group-hover:text-white transition-colors" />
                          </div>

                          {/* Orbiting Nodes */}
                          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-6 w-3 h-3 bg-blue-400 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.8)] animate-bounce delay-75"></div>
                          <div className="absolute bottom-0 right-1/4 w-2 h-2 bg-purple-400 rounded-full shadow-[0_0_10px_rgba(168,85,247,0.8)] animate-pulse"></div>
                          <div className="absolute bottom-1/4 left-0 w-2 h-2 bg-indigo-400 rounded-full shadow-[0_0_10px_rgba(99,102,241,0.8)] animate-pulse delay-100"></div>
                      </div>

                      <div className="max-w-[380px] space-y-4">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-[10px] font-bold text-blue-500 uppercase tracking-widest mb-2">
                           <LucideIcons.Cpu className="w-3 h-3" /> v2.0 Neural Engine
                        </div>
                        <h3 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-blue-800 to-gray-900 dark:from-white dark:via-blue-200 dark:to-white tracking-tight">
                            Ryze Neural Engine
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed font-medium">
                            The world's first <span className="text-blue-500 font-bold">Deterministic AI</span> for UI generation. 
                            Zero hallucinations. 100% valid React code.
                        </p>
                      </div>

                      <div className="grid grid-cols-2 gap-2 w-full max-w-xs">
                          {["Dashboard", "Landing Page", "Login Screen", "Contact Form"].map((tag, i) => (
                              <button 
                                key={tag} 
                                onClick={() => setInput(`Create a ${tag.toLowerCase()} tailored for a tech startup`)} 
                                className="text-xs font-medium bg-white dark:bg-gray-900/50 hover:bg-blue-50 dark:hover:bg-blue-900/20 px-4 py-3 rounded-xl transition-all border border-gray-200 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-800 shadow-sm hover:shadow-md text-left flex items-center justify-between group"
                                style={{ animationDelay: `${i * 100}ms` }}
                              >
                                  {tag}
                                  <LucideIcons.ArrowRight className="w-3 h-3 opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all text-blue-500" />
                              </button>
                          ))}
                      </div>
                  </div>
                  
              )}

              {/* Chat Messages or Empty State */}
              {history.length === 0 ? (
                  <div className="flex-1 flex flex-col items-center justify-center p-6 text-center space-y-8 animate-in fade-in zoom-in-95 duration-500">
                      <div className="relative group">
                          <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-xl group-hover:bg-blue-500/30 transition-all"></div>
                          <div className="relative bg-white dark:bg-gray-900/80 p-6 rounded-2xl ring-1 ring-gray-200 dark:ring-gray-800 shadow-xl">
                              <Bot className="w-12 h-12 text-blue-600 dark:text-blue-400" />
                          </div>
                      </div>
                      
                      <div className="max-w-md space-y-2">
                          <h3 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
                             What can I build for you?
                          </h3>
                          <p className="text-muted-foreground text-sm">
                             I generate production-ready React components. Try one of these examples:
                          </p>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
                          {[
                              { icon: Layout, label: "SaaS Landing Page", prompt: "Create a modern SaaS landing page for a startup called Nexus" },
                              { icon: ShoppingBag, label: "E-commerce Product", prompt: "Design a product page for a premium sneaker brand" },
                              { icon: Users, label: "Developer Portfolio", prompt: "Create a minimal portfolio for a developer named Alex" },
                              { icon: MonitorPlay, label: "Admin Dashboard", prompt: "Build a dark mode analytics dashboard with charts" }
                          ].map((item, i) => (
                              <button 
                                  key={i}
                                  onClick={() => setInput(item.prompt)}
                                  className="flex items-center gap-3 p-4 text-left bg-white dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-xl hover:border-blue-500 dark:hover:border-blue-500 hover:shadow-md transition-all group"
                              >
                                  <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg group-hover:bg-blue-500/10 group-hover:text-blue-600 transition-colors">
                                      <item.icon className="w-4 h-4" />
                                  </div>
                                  <span className="text-xs font-medium text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white transition-colors">{item.label}</span>
                              </button>
                          ))}
                      </div>
                  </div>
              ) : (
                  <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-hide">
                      {history.map((item, idx) => (
                          <div key={idx} className={`flex flex-col ${item.role === 'user' ? 'items-end' : 'items-start'} animate-in slide-in-from-bottom-2 fade-in duration-300`}>
                              <div className={`
                                 max-w-[90%] rounded-2xl px-5 py-3.5 text-sm shadow-sm backdrop-blur-sm
                                 ${item.role === 'user' 
                                   ? 'bg-blue-600 text-white rounded-br-sm shadow-blue-500/10' 
                                   : 'bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 rounded-bl-sm border border-gray-200/50 dark:border-gray-800/50 shadow-lg'
                                 }
                              `}>
                                 {item.role === 'user' ? item.content : (
                                     <div className="space-y-3">
                                        <div className="flex items-center gap-2 mb-2 pb-2 border-b border-gray-100 dark:border-gray-800">
                                            <div className="w-4 h-4 rounded bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                                                <LucideIcons.Sparkles className="w-2.5 h-2.5 text-white" />
                                            </div>
                                            <span className="font-bold text-[10px] uppercase tracking-wider text-gray-500">Ryze AI</span>
                                        </div>
                                        <p className="whitespace-pre-wrap leading-relaxed">{item.explanation}</p>
                                     </div>
                                 )}
                              </div>
                              <span className="text-[10px] text-gray-400 mt-1.5 px-1 font-mono opacity-60">
                                  {new Date(item.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                              </span>
                          </div>
                      ))}
                      <div ref={chatEndRef} />
                  </div>
              )}
              
              {loading && (
                 <div className="px-6 py-2 flex items-center gap-2 text-xs text-blue-500 font-medium animate-pulse">
                    <Loader2 className="w-3 h-3 animate-spin"/>
                    <span>Generating UI...</span>
                 </div>
              )}
              <div ref={chatEndRef} />
           </div>

           {/* Input Area */}
           <div className="p-4 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-black">
              <div className="relative">
                 <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleGenerate();
                        }
                    }}
                    placeholder="Describe your UI..."
                    className="w-full resize-none rounded-xl border border-gray-300 bg-gray-50 p-3 pr-20 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-800 dark:bg-gray-900 dark:text-white"
                    rows={3}
                 />
                 <div className="absolute bottom-3 right-3 flex gap-2">
                     <button
                        onClick={handleVoiceInput}
                        className="rounded-lg bg-gray-200 dark:bg-gray-800 p-2 text-gray-600 dark:text-gray-400 hover:text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all"
                        title="Voice Input"
                     >
                        <LucideIcons.Mic className="h-4 w-4" />
                     </button>
                     <button 
                        onClick={() => handleGenerate()}
                        disabled={loading || !input.trim()}
                        className="rounded-lg bg-blue-600 p-2 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                     >
                        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                     </button>
                 </div>
              </div>
           </div>
        </section>

        {/* Right Panel: Preview & Code */}
        <section className="flex flex-1 flex-col bg-gray-50 dark:bg-[#0A0A0A] overflow-hidden">
            {/* Tabs */}
            <div className="flex items-center justify-between border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-black px-4 h-12">
               <div className="flex items-center gap-6 h-full">
                  <button 
                     onClick={() => setActiveTab('preview')}
                     className={`flex items-center gap-2 h-full text-sm font-medium border-b-2 transition-colors ${activeTab === 'preview' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'}`}
                  >
                     <Eye className="h-4 w-4" /> Preview
                  </button>
                  <button 
                     onClick={() => setActiveTab('code')}
                     className={`flex items-center gap-2 h-full text-sm font-medium border-b-2 transition-colors ${activeTab === 'code' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'}`}
                  >
                     <Code className="h-4 w-4" /> Code
                  </button>
                  <button 
                     onClick={() => setActiveTab('plan')}
                     className={`flex items-center gap-2 h-full text-sm font-medium border-b-2 transition-colors ${activeTab === 'plan' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'}`}
                  >
                     <History className="h-4 w-4" /> Plan
                  </button>
               </div>
               
               <div className="text-xs text-gray-400 flex items-center gap-2">
                  {status && <span className="animate-pulse text-blue-500">{status}</span>}
                  {currentStep >= 0 && <span className="hidden sm:inline-block">Generated matching Component Library</span>}
               </div>
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-hidden relative">
               {activeTab === 'preview' && (
                  <div className="h-full w-full p-4 md:p-8 overflow-auto">
                     <Preview code={currentCode} isFullScreen={isFullScreen} setIsFullScreen={setIsFullScreen} handleCopyCode={handleCopyCode} handleDownloadCode={handleDownloadCode} handleDeploy={handleDeploy} />
                  </div>
               )}

               {activeTab === 'code' && (
                  <div className="h-full w-full bg-[#1e1e1e] text-white overflow-hidden flex flex-col font-mono text-sm relative">
                     {/* Code Toolbar */}
                     <div className="flex items-center justify-between px-4 py-2 bg-[#252526] border-b border-[#3e3e42]">
                        <div className="flex items-center gap-2">
                            <button 
                               onClick={handleCopyCode}
                               className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded transition-colors"
                               title="Copy Code"
                            >
                               <LucideIcons.Copy className="w-4 h-4" />
                            </button>
                            <button 
                               onClick={handleDownloadCode}
                               className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded transition-colors"
                               title="Download File"
                            >
                               <LucideIcons.Download className="w-4 h-4" />
                            </button>
                            <button 
                               onClick={handleGithubExport}
                               className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded transition-colors"
                               title="Export to GitHub"
                            >
                               <LucideIcons.Github className="w-4 h-4" />
                            </button>
                        </div>
                        <button 
                           onClick={() => {
                               const prompt = "Refactor this code for better performance and readability";
                               setInput(prompt);
                               handleGenerate(prompt);
                           }}
                           className="flex items-center gap-2 text-xs text-white bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded transition-colors shadow-lg shadow-blue-500/20"
                        >
                           <LucideIcons.Sparkles className="w-3 h-3" /> AI Refactor
                        </button>
                     </div>
                     
                     <textarea 
                        className="flex-1 w-full bg-[#1e1e1e] p-4 font-mono text-sm resize-none focus:outline-none text-[#d4d4d4]"
                        value={currentCode}
                        onChange={(e) => handleCodeEdit(e.target.value)}
                        spellCheck="false"
                     />
                     {/* VS Code Style Status Bar */}
                     <div className="h-6 bg-[#007acc] w-full flex items-center justify-between px-3 text-[10px] select-none z-20 text-white">
                        <div className="flex gap-4">
                           <span className="flex items-center gap-1"><LucideIcons.GitBranch className="w-3 h-3"/> main</span>
                           <span className="flex items-center gap-1"><LucideIcons.CheckCircle className="w-3 h-3"/> Ready</span>
                        </div>
                        <div className="flex gap-4">
                           <span>Ln {currentCode.split('\n').length}, Col 1</span>
                           <span>UTF-8</span>
                           <span>JavaScript JSX</span>
                           <span className="hover:bg-white/20 px-1 rounded cursor-pointer transition-colors"><LucideIcons.Bell className="w-3 h-3"/></span>
                        </div>
                     </div>
                  </div>
               )}

                {activeTab === 'plan' && (
                  <div className="h-full w-full bg-white dark:bg-black p-8 overflow-auto text-sm font-mono whitespace-pre-wrap text-gray-700 dark:text-gray-300">
                     {currentPlan || "No plan available."}
                  </div>
               )}
            </div>
        </section>
      </main>



      {/* Professional Footer */}
      <footer className="fixed bottom-0 right-0 p-2 text-[10px] text-gray-400 opacity-30 hover:opacity-100 transition-opacity z-10 pointer-events-none">
         Ryze AI v2.0 • Deterministic Engine Active • Press Cmd+K to chat
      </footer>
    </div>
  );
}
