const express = require('express');
const router = express.Router();
const generatorController = require('../controllers/generator.controller.js');

// Generate new UI
router.post('/generate', generatorController.generateUI);

// Modify existing UI
router.post('/modify', generatorController.modifyUI);

// Persist and share a generated UI (returns shareable slug / URL)
router.post('/share', generatorController.shareUI);

// Public read-only endpoint for shared UIs
router.get('/share/:slug', generatorController.getSharedUI);

// Persistent Deployment (HTML Storage)
router.post('/deploy', generatorController.deployUI);
router.get('/view/:id', generatorController.viewDeployment);
router.get('/download/:id', generatorController.downloadDeployment);

module.exports = router;
