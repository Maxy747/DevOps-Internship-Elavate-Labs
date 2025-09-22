const request = require('supertest');
const { app, server } = require('./server'); // Import both app and server

describe('GET /', () => {
  it('responds with Hello Darling!', (done) => {
    request(app)
      .get('/')
      .expect('Hello Darling! the CI/CD pipeline is working!', done);
  });
});

// This will run after all tests in this file have finished
afterAll((done) => {
  server.close(done); // Close the server
});