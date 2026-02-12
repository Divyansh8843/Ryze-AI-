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
