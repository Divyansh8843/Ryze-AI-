const express = require('express');
const axios = require('axios');
const cors = require('cors');
const dotenv = require('dotenv');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const connectDB = require('./config/db');
const generatorRoutes = require('./routes/generator.routes');
const githubRoutes = require('./routes/github.routes');

// Load env vars
dotenv.config();

// Connect to Database
// Note: Optional for this architecture, but included for complete MERN stack compliance.
connectDB();

const app = express();

// Security & Performance Middleware
app.enable('trust proxy'); // Ensure req.protocol detects HTTPS on Render/Vercel
app.use(helmet());
app.use(compression());
app.use(morgan('dev')); // Logger
app.use((req, res, next) => {
  console.log(`[DEBUG] Received ${req.method} request for ${req.url} at ${new Date().toISOString()}`);
  next();
});


// CORS Configuration
app.use(cors({
  origin: [
    'http://localhost:5173', 
    'http://127.0.0.1:5173', 
    'https://ryze-ai-agent.vercel.app', // Explicit Vercel Domain
    process.env.FRONTEND_URL // Dynamic Env Var
  ].filter(Boolean),
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  credentials: true
}));

app.use(express.json({ limit: '50mb' }));

// Routes
app.use('/api/generator', generatorRoutes);
app.use('/api/github', githubRoutes);

// Reverse Proxy to Python AI Service (Port 5001) for Direct Access
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5001';

const generatorController = require('./controllers/generator.controller');

// Persistent Deployment Routes (Handled by Node Controller + MongoDB)
app.post('/deploy', generatorController.deployUI);
app.get('/view/:id', generatorController.viewDeployment);
app.get('/download/:id', generatorController.downloadDeployment);

// Direct AI Service Proxies (kept for legacy/direct access if needed, but primary flow is via /api/generator)
// Note: Frontend uses /api/generator/generate and /api/generator/modify provided by generatorRoutes


// Health Check
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'success', 
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Root Route
app.get('/', (req, res) => {
  res.send('Ryze AI API Gateway is running securely.');
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('[Global Error]', err.stack);
  res.status(500).json({ 
    success: false, 
    error: 'Internal Server Error', 
    message: process.env.NODE_ENV === 'development' ? err.message : undefined 
  });
});

const PORT = process.env.PORT || 5000;

const server = app.listen(PORT, () => {
  console.log(`🚀 API Gateway running on port ${PORT}`);
  console.log(`🔗 Connected to AI Service at ${process.env.AI_SERVICE_URL || 'http://localhost:5001'}`);
});

// Increase timeout to 5 minutes (300000ms) to accommodate Render cold starts
server.setTimeout(300000);
