const express = require('express');
const router = express.Router();
const githubController = require('../controllers/github.controller');

// Export current generated UI code into a new GitHub repo
router.post('/export', githubController.exportToGitHub);

module.exports = router;

