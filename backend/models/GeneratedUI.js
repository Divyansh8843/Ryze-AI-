const mongoose = require('mongoose');

const UISchema = new mongoose.Schema({
  prompt: {
    type: String,
    required: true,
  },
  code: {
    type: String,
    required: true,
  },
  intent: {
    type: String,
    default: 'dashboard',
  },
  plan: {
    type: String,
  },
  explanation: {
    type: String,
  },
  slug: {
    type: String,
    unique: true,
    sparse: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('GeneratedUI', UISchema);
