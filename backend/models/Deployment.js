const mongoose = require('mongoose');

const DeploymentSchema = new mongoose.Schema({
  originalCode: {
    type: String,
    required: true
  },
  htmlContent: {
    type: String, // Full standalone HTML string
    required: true
  },
  prompt: {
    type: String,
    required: false
  },
  title: {
    type: String,
    required: false
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Deployment', DeploymentSchema);
