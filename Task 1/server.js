const express = require('express');
const app = express();
const PORT = 8080;

app.get('/', (req, res) => {
  res.send('Hello Darling! the CI/CD pipeline is working!');
});

// Start the server and export it so we can close it in our tests
const server = app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

module.exports = { app, server }; // Export both the app and the server