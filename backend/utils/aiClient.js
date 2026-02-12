const OpenAI = require('openai');
const dotenv = require('dotenv');

dotenv.config();

let openai;

try {
  if (process.env.OPENAI_API_KEY) {
    openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  } else {
    console.warn("OPENAI_API_KEY not found in environment variables. AI features will not work.");
  }
} catch (error) {
  console.error("Error initializing OpenAI client:", error);
}

module.exports = openai;
