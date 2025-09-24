// server.js
const express = require('express');
const morgan = require('morgan');  // For clean request logging
const helmet = require('helmet');  // For security headers
const cors = require('cors');      // For cross-origin support

const app = express();
const port = process.env.PORT || 8080;

// --- Middleware ---
app.use(express.json());   // Parse JSON requests
app.use(cors());           // Enable CORS
app.use(helmet());         // Secure HTTP headers
app.use(morgan('dev'));    // Log requests in dev format

// --- Routes ---
app.get('/', (req, res) => {
  res.json({
    message: '🚀 Welcome to the Sleek Express Server!',
    status: 'OK',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/hello/:name', (req, res) => {
  res.json({
    greeting: `Hello, ${req.params.name}! 👋`,
    tip: 'Try visiting /api/status to check server health.'
  });
});

app.get('/api/status', (req, res) => {
  res.json({
    uptime: process.uptime(),
    message: 'Server is running smoothly ✅',
    date: new Date()
  });
});

// --- Error Handling ---
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'The requested resource does not exist.'
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

// --- Start Server ---
app.listen(port, () => {
  console.log(`⚡ Server running at: http://localhost:${port}`);
});
