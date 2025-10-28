from flask import Flask

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def hello():
    """Returns a simple 'Hello, World!' message."""
    return "Hello, World! This is my Python app running in Docker."

if __name__ == '__main__':
    # Run the app on host 0.0.0.0 to make it accessible
    # outside the container.
    app.run(host='0.0.0.0', port=5000)