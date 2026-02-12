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
app.use(helmet());
app.use(compression());
app.use(morgan('dev')); // Logger

// CORS Configuration
app.use(cors({
  origin: ['http://localhost:5173', 'http://127.0.0.1:5173', process.env.FRONTEND_URL],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  credentials: true
}));

app.use(express.json());

// Routes
app.use('/api/generator', generatorRoutes);
app.use('/api/github', githubRoutes);

// Reverse Proxy to Python AI Service (Port 5001) for Direct Access
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5001';

// Proxy Deployment Request
app.post('/deploy', async (req, res) => {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/deploy`, req.body);
    res.json(response.data);
  } catch (error) {
    console.error('[Proxy Error] /deploy:', error.message);
    res.status(500).json({ error: 'Deployment Service Unavailable' });
  }
});

// Proxy View Request (HTML Content)
app.get('/view/:filename', async (req, res) => {
  try {
    const response = await axios.get(`${AI_SERVICE_URL}/view/${req.params.filename}`, {
      responseType: 'arraybuffer' // Handle binary/text content correctly
    });
    res.set(response.headers);
    res.send(response.data);
  } catch (error) {
    console.error('[Proxy Error] /view:', error.message);
    res.status(404).send('Deployment Not Found');
  }
});

// Proxy Generate Request (for direct /generate calls)
app.post('/generate', async (req, res) => {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/generate`, req.body);
    res.json(response.data);
  } catch (error) {
    console.error('[Proxy Error] /generate:', error.message);
    res.status(500).json({ error: 'Generation Service Unavailable' });
  }
});

// Proxy Modify Request (for AI Refactoring/Edits)
app.post('/modify', async (req, res) => {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/modify`, req.body);
    res.json(response.data);
  } catch (error) {
    console.error('[Proxy Error] /modify:', error.message);
    res.status(500).json({ error: 'Modification Service Unavailable' });
  }
});

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

app.listen(PORT, () => {
  console.log(`🚀 API Gateway running on port ${PORT}`);
  console.log(`🔗 Connected to AI Service at ${process.env.AI_SERVICE_URL || 'http://localhost:5001'}`);
});
