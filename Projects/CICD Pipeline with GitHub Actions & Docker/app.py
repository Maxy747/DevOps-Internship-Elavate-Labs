from flask import Flask, jsonify, request, render_template_string
from functools import wraps
import logging
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory data store (use Redis/PostgreSQL in production)
data_store = {
    'visits': 0,
    'users': [],
    'messages': []
}

# Middleware - Request logging
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")
    data_store['visits'] += 1

# Middleware - Response headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key'
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

# Decorator for API key authentication
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        valid_key = os.environ.get('API_KEY', 'demo-api-key')
        if api_key != valid_key:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask API</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
                color: #1a202c;
            }
            
            .container {
                max-width: 900px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                margin-bottom: 60px;
                animation: fadeInDown 0.8s ease;
            }
            
            .logo {
                width: 80px;
                height: 80px;
                background: white;
                border-radius: 20px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                margin-bottom: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            
            h1 {
                color: white;
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 10px;
                letter-spacing: -1px;
            }
            
            .subtitle {
                color: rgba(255,255,255,0.9);
                font-size: 18px;
                font-weight: 400;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
                animation: fadeInUp 0.8s ease 0.2s both;
            }
            
            .stat-card {
                background: rgba(255,255,255,0.95);
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            
            .stat-label {
                color: #718096;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
                font-weight: 600;
            }
            
            .stat-value {
                color: #667eea;
                font-size: 32px;
                font-weight: 700;
            }
            
            .endpoints-section {
                animation: fadeInUp 0.8s ease 0.4s both;
            }
            
            .section-title {
                color: white;
                font-size: 24px;
                font-weight: 600;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .endpoint-card {
                background: rgba(255,255,255,0.95);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border-left: 4px solid transparent;
            }
            
            .endpoint-card:hover {
                transform: translateX(5px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
                border-left-color: #667eea;
            }
            
            .endpoint-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 12px;
                flex-wrap: wrap;
            }
            
            .method {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            
            .method.get { background: #48bb78; color: white; }
            .method.post { background: #4299e1; color: white; }
            .method.delete { background: #f56565; color: white; }
            
            .endpoint-path {
                font-family: 'Monaco', 'Courier New', monospace;
                background: #f7fafc;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 14px;
                color: #2d3748;
                font-weight: 500;
                flex: 1;
                min-width: 200px;
            }
            
            .endpoint-description {
                color: #4a5568;
                font-size: 15px;
                line-height: 1.6;
            }
            
            .badge {
                display: inline-block;
                padding: 4px 10px;
                background: #fef5e7;
                color: #d97706;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 8px;
            }
            
            .endpoint-btn {
                display: inline-block;
                margin-top: 12px;
                padding: 10px 20px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .endpoint-btn:hover {
                transform: translateX(5px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .footer {
                text-align: center;
                margin-top: 60px;
                color: rgba(255,255,255,0.8);
                font-size: 14px;
                animation: fadeIn 0.8s ease 0.6s both;
            }
            
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @media (max-width: 768px) {
                h1 { font-size: 36px; }
                .stats-grid { grid-template-columns: 1fr; }
                .endpoint-header { flex-direction: column; align-items: flex-start; }
                .endpoint-path { width: 100%; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀</div>
                <h1>Flask API</h1>
                <p class="subtitle">Modern RESTful API with authentication & monitoring</p>
            </div>
            
            <div class="stats-grid" id="stats">
                <div class="stat-card">
                    <div class="stat-label">Total Visits</div>
                    <div class="stat-value" id="visits">""" + str(data_store['visits']) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Users</div>
                    <div class="stat-value" id="users">""" + str(len(data_store['users'])) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Messages</div>
                    <div class="stat-value" id="messages">""" + str(len(data_store['messages'])) + """</div>
                </div>
            </div>
            
            <div class="endpoints-section">
                <h2 class="section-title">📡 API Endpoints</h2>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <code class="endpoint-path">/api/health</code>
                    </div>
                    <p class="endpoint-description">Health check endpoint for monitoring service status</p>
                    <a href="/api/health" class="endpoint-btn">View Page →</a>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <code class="endpoint-path">/api/stats</code>
                    </div>
                    <p class="endpoint-description">Retrieve application statistics and metrics</p>
                    <a href="/api/stats" class="endpoint-btn">View Page →</a>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method post">POST</span>
                        <code class="endpoint-path">/api/users</code>
                    </div>
                    <p class="endpoint-description">Create a new user account (requires: name, email)</p>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <code class="endpoint-path">/api/users</code>
                    </div>
                    <p class="endpoint-description">List all registered users</p>
                    <a href="/api/users" class="endpoint-btn">View Page →</a>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <code class="endpoint-path">/api/users/:id</code>
                    </div>
                    <p class="endpoint-description">Get details of a specific user by ID</p>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method delete">DELETE</span>
                        <code class="endpoint-path">/api/users/:id</code>
                    </div>
                    <p class="endpoint-description">Delete a user account</p>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method post">POST</span>
                        <code class="endpoint-path">/api/messages</code>
                        <span class="badge">🔐 AUTH</span>
                    </div>
                    <p class="endpoint-description">Post a new message (requires X-API-Key header)</p>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <code class="endpoint-path">/api/messages</code>
                        <span class="badge">🔐 AUTH</span>
                    </div>
                    <p class="endpoint-description">Retrieve all messages (requires X-API-Key header)</p>
                    <a href="/api/messages" class="endpoint-btn">View Page →</a>
                </div>
                
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <code class="endpoint-path">/api/search?q=query</code>
                    </div>
                    <p class="endpoint-description">Search users by name</p>
                    <a href="/api/search" class="endpoint-btn">View Page →</a>
                </div>
            </div>
            
            <div class="footer">
                <p>Built with Flask • Python • Docker</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Health Check</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: rgba(255,255,255,0.95);
                border-radius: 24px;
                padding: 60px 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                text-align: center;
                max-width: 500px;
                animation: fadeInScale 0.6s ease;
            }
            .status-icon {
                width: 100px;
                height: 100px;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 50px;
                margin: 0 auto 30px;
                animation: pulse 2s ease-in-out infinite;
            }
            h1 {
                color: #1a202c;
                font-size: 36px;
                margin-bottom: 15px;
                font-weight: 700;
            }
            .subtitle {
                color: #4a5568;
                font-size: 18px;
                margin-bottom: 40px;
            }
            .info-grid {
                display: grid;
                gap: 15px;
                text-align: left;
            }
            .info-item {
                background: #f7fafc;
                padding: 15px 20px;
                border-radius: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .info-label {
                color: #718096;
                font-weight: 600;
                font-size: 14px;
            }
            .info-value {
                color: #2d3748;
                font-weight: 600;
                font-family: 'Monaco', monospace;
                font-size: 14px;
            }
            .back-btn {
                margin-top: 30px;
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(17, 153, 142, 0.3);
            }
            @keyframes fadeInScale {
                from {
                    opacity: 0;
                    transform: scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status-icon">✓</div>
            <h1>System Healthy</h1>
            <p class="subtitle">All systems operational</p>
            <div class="info-grid" id="healthData"></div>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
        <script>
            const data = """ + json.dumps({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': '1.0.0',
                'environment': os.environ.get('ENVIRONMENT', 'development')
            }) + """;
            const grid = document.getElementById('healthData');
            Object.keys(data).forEach(key => {
                const item = document.createElement('div');
                item.className = 'info-item';
                item.innerHTML = `
                    <span class="info-label">${key.toUpperCase()}</span>
                    <span class="info-value">${data[key]}</span>
                `;
                grid.appendChild(item);
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Statistics</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 50px;
                animation: fadeInDown 0.6s ease;
            }
            h1 {
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 10px;
            }
            .subtitle {
                font-size: 18px;
                opacity: 0.95;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
                animation: fadeInUp 0.6s ease 0.2s both;
            }
            .stat-card {
                background: rgba(255,255,255,0.95);
                padding: 35px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                transition: transform 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            .stat-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #f093fb, #f5576c);
            }
            .stat-card:hover {
                transform: translateY(-8px);
            }
            .stat-icon {
                font-size: 40px;
                margin-bottom: 15px;
            }
            .stat-label {
                color: #718096;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 10px;
            }
            .stat-value {
                color: #2d3748;
                font-size: 42px;
                font-weight: 700;
                line-height: 1;
            }
            .details-card {
                background: rgba(255,255,255,0.95);
                padding: 35px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                animation: fadeInUp 0.6s ease 0.4s both;
            }
            .details-grid {
                display: grid;
                gap: 15px;
            }
            .detail-item {
                display: flex;
                justify-content: space-between;
                padding: 15px;
                background: #f7fafc;
                border-radius: 10px;
                align-items: center;
            }
            .detail-label {
                color: #4a5568;
                font-weight: 600;
            }
            .detail-value {
                color: #2d3748;
                font-family: 'Monaco', monospace;
                font-size: 14px;
                font-weight: 600;
            }
            .back-btn {
                margin-top: 30px;
                display: inline-block;
                padding: 14px 35px;
                background: white;
                color: #f5576c;
                text-decoration: none;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            .back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Statistics</h1>
                <p class="subtitle">Real-time application metrics</p>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-label">Total Users</div>
                    <div class="stat-value">""" + str(len(data_store['users'])) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">💬</div>
                    <div class="stat-label">Messages</div>
                    <div class="stat-value">""" + str(len(data_store['messages'])) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">👁️</div>
                    <div class="stat-label">Total Visits</div>
                    <div class="stat-value">""" + str(data_store['visits']) + """</div>
                </div>
            </div>
            <div class="details-card">
                <h2 style="margin-bottom: 25px; color: #2d3748;">System Information</h2>
                <div class="details-grid">
                    <div class="detail-item">
                        <span class="detail-label">Current Time (UTC)</span>
                        <span class="detail-value">""" + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + """</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Environment</span>
                        <span class="detail-value">""" + os.environ.get('ENVIRONMENT', 'development') + """</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">API Version</span>
                        <span class="detail-value">1.0.0</span>
                    </div>
                </div>
                <a href="/" class="back-btn">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    """User management endpoint"""
    if request.method == 'GET':
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Users</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    color: white;
                    margin-bottom: 50px;
                    animation: fadeInDown 0.6s ease;
                }
                h1 {
                    font-size: 48px;
                    font-weight: 700;
                    margin-bottom: 10px;
                }
                .subtitle {
                    font-size: 18px;
                    opacity: 0.95;
                }
                .action-bar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                    flex-wrap: wrap;
                    gap: 15px;
                    animation: fadeInUp 0.6s ease 0.2s both;
                }
                .user-count {
                    background: rgba(255,255,255,0.2);
                    padding: 12px 25px;
                    border-radius: 12px;
                    color: white;
                    font-weight: 600;
                    backdrop-filter: blur(10px);
                }
                .add-btn {
                    padding: 12px 30px;
                    background: white;
                    color: #667eea;
                    border: none;
                    border-radius: 12px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                }
                .add-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                }
                .users-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                    gap: 25px;
                    animation: fadeInUp 0.6s ease 0.4s both;
                }
                .user-card {
                    background: rgba(255,255,255,0.95);
                    padding: 30px;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                    transition: transform 0.3s ease;
                    position: relative;
                }
                .user-card:hover {
                    transform: translateY(-5px);
                }
                .user-avatar {
                    width: 70px;
                    height: 70px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 28px;
                    font-weight: 700;
                    margin-bottom: 20px;
                }
                .user-name {
                    color: #2d3748;
                    font-size: 22px;
                    font-weight: 700;
                    margin-bottom: 8px;
                }
                .user-email {
                    color: #718096;
                    font-size: 14px;
                    margin-bottom: 15px;
                }
                .user-meta {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding-top: 15px;
                    border-top: 1px solid #e2e8f0;
                }
                .user-id {
                    color: #a0aec0;
                    font-size: 13px;
                    font-weight: 600;
                }
                .user-date {
                    color: #a0aec0;
                    font-size: 12px;
                }
                .empty-state {
                    text-align: center;
                    padding: 80px 20px;
                    background: rgba(255,255,255,0.95);
                    border-radius: 20px;
                    animation: fadeInUp 0.6s ease 0.4s both;
                }
                .empty-icon {
                    font-size: 80px;
                    margin-bottom: 20px;
                    opacity: 0.5;
                }
                .empty-text {
                    color: #4a5568;
                    font-size: 18px;
                    margin-bottom: 30px;
                }
                .back-btn {
                    margin-top: 30px;
                    display: inline-block;
                    padding: 14px 35px;
                    background: white;
                    color: #667eea;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                .back-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
                }
                @keyframes fadeInDown {
                    from { opacity: 0; transform: translateY(-30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>👥 Users</h1>
                    <p class="subtitle">Manage all registered users</p>
                </div>
                <div class="action-bar">
                    <div class="user-count">Total Users: """ + str(len(data_store['users'])) + """</div>
                    <a href="/" class="back-btn">← Back to Home</a>
                </div>
                """ + ("""
                <div class="users-grid">
                """ + ''.join([f"""
                    <div class="user-card">
                        <div class="user-avatar">{user['name'][0].upper()}</div>
                        <div class="user-name">{user['name']}</div>
                        <div class="user-email">{user['email']}</div>
                        <div class="user-meta">
                            <span class="user-id">ID: {user['id']}</span>
                            <span class="user-date">{user['created_at'][:10]}</span>
                        </div>
                    </div>
                """ for user in data_store['users']]) + """
                </div>
                """ if data_store['users'] else """
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <div class="empty-text">No users yet</div>
                    <p style="color: #718096;">Create your first user using the POST /api/users endpoint</p>
                </div>
                """) + """
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        user = {
            'id': len(data_store['users']) + 1,
            'name': data['name'],
            'email': data['email'],
            'created_at': datetime.utcnow().isoformat()
        }
        
        data_store['users'].append(user)
        logger.info(f"New user created: {user['name']}")
        
        return jsonify({
            'message': 'User created successfully',
            'user': user
        }), 201

@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_detail(user_id):
    """Get or delete a specific user"""
    user = next((u for u in data_store['users'] if u['id'] == user_id), None)
    
    if not user:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Not Found</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .container {
                    background: rgba(255,255,255,0.95);
                    border-radius: 24px;
                    padding: 60px 40px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                    text-align: center;
                    max-width: 500px;
                    animation: shake 0.5s ease;
                }
                .error-icon {
                    font-size: 80px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #2d3748;
                    font-size: 32px;
                    margin-bottom: 15px;
                }
                .message {
                    color: #718096;
                    font-size: 16px;
                    margin-bottom: 30px;
                }
                .back-btn {
                    padding: 14px 35px;
                    background: linear-gradient(135deg, #f093fb, #f5576c);
                    color: white;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 600;
                    display: inline-block;
                    transition: transform 0.3s ease;
                }
                .back-btn:hover {
                    transform: translateY(-2px);
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-10px); }
                    75% { transform: translateX(10px); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error-icon">🔍</div>
                <h1>User Not Found</h1>
                <p class="message">The user with ID """ + str(user_id) + """ doesn't exist in our database.</p>
                <a href="/api/users" class="back-btn">← View All Users</a>
            </div>
        </body>
        </html>
        """
        return render_template_string(html), 404
    
    if request.method == 'GET':
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Details</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .container {
                    max-width: 600px;
                    width: 100%;
                }
                .user-card {
                    background: rgba(255,255,255,0.95);
                    border-radius: 24px;
                    padding: 50px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                    animation: fadeInScale 0.6s ease;
                }
                .user-avatar {
                    width: 120px;
                    height: 120px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 48px;
                    font-weight: 700;
                    margin: 0 auto 30px;
                }
                .user-name {
                    text-align: center;
                    color: #2d3748;
                    font-size: 36px;
                    font-weight: 700;
                    margin-bottom: 10px;
                }
                .user-email {
                    text-align: center;
                    color: #718096;
                    font-size: 18px;
                    margin-bottom: 40px;
                }
                .info-grid {
                    display: grid;
                    gap: 15px;
                    margin-bottom: 30px;
                }
                .info-item {
                    display: flex;
                    justify-content: space-between;
                    padding: 20px;
                    background: #f7fafc;
                    border-radius: 12px;
                    align-items: center;
                }
                .info-label {
                    color: #4a5568;
                    font-weight: 600;
                }
                .info-value {
                    color: #2d3748;
                    font-family: 'Monaco', monospace;
                    font-weight: 600;
                }
                .actions {
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                }
                .btn {
                    padding: 14px 30px;
                    border: none;
                    border-radius: 12px;
                    font-weight: 600;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    transition: all 0.3s ease;
                }
                .btn-back {
                    background: #e2e8f0;
                    color: #2d3748;
                }
                .btn-back:hover {
                    background: #cbd5e0;
                    transform: translateY(-2px);
                }
                @keyframes fadeInScale {
                    from {
                        opacity: 0;
                        transform: scale(0.9);
                    }
                    to {
                        opacity: 1;
                        transform: scale(1);
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="user-card">
                    <div class="user-avatar">""" + user['name'][0].upper() + """</div>
                    <div class="user-name">""" + user['name'] + """</div>
                    <div class="user-email">""" + user['email'] + """</div>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">User ID</span>
                            <span class="info-value">""" + str(user['id']) + """</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Created At</span>
                            <span class="info-value">""" + user['created_at'][:19].replace('T', ' ') + """</span>
                        </div>
                    </div>
                    <div class="actions">
                        <a href="/api/users" class="btn btn-back">← Back to Users</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    
    elif request.method == 'DELETE':
        data_store['users'] = [u for u in data_store['users'] if u['id'] != user_id]
        logger.info(f"User deleted: {user_id}")
        return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/api/messages', methods=['GET', 'POST'])
@require_api_key
def messages():
    """Protected endpoint for messages"""
    if request.method == 'GET':
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Messages</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }
                .container {
                    max-width: 900px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    color: white;
                    margin-bottom: 50px;
                    animation: fadeInDown 0.6s ease;
                }
                h1 {
                    font-size: 48px;
                    font-weight: 700;
                    margin-bottom: 10px;
                }
                .subtitle {
                    font-size: 18px;
                    opacity: 0.95;
                }
                .lock-badge {
                    display: inline-block;
                    background: rgba(255,255,255,0.3);
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-size: 14px;
                    margin-top: 10px;
                    backdrop-filter: blur(10px);
                }
                .action-bar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                    animation: fadeInUp 0.6s ease 0.2s both;
                }
                .message-count {
                    background: rgba(255,255,255,0.95);
                    padding: 12px 25px;
                    border-radius: 12px;
                    color: #2d3748;
                    font-weight: 600;
                }
                .back-btn {
                    padding: 12px 30px;
                    background: white;
                    color: #fa709a;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                .back-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                }
                .messages-container {
                    animation: fadeInUp 0.6s ease 0.4s both;
                }
                .message-card {
                    background: rgba(255,255,255,0.95);
                    padding: 30px;
                    border-radius: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease;
                    border-left: 5px solid #fa709a;
                }
                .message-card:hover {
                    transform: translateX(5px);
                }
                .message-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                }
                .message-author {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .author-avatar {
                    width: 45px;
                    height: 45px;
                    background: linear-gradient(135deg, #fa709a, #fee140);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 700;
                    font-size: 18px;
                }
                .author-name {
                    color: #2d3748;
                    font-weight: 700;
                    font-size: 18px;
                }
                .message-date {
                    color: #a0aec0;
                    font-size: 13px;
                }
                .message-content {
                    color: #4a5568;
                    line-height: 1.6;
                    font-size: 16px;
                }
                .empty-state {
                    text-align: center;
                    padding: 80px 20px;
                    background: rgba(255,255,255,0.95);
                    border-radius: 20px;
                }
                .empty-icon {
                    font-size: 80px;
                    margin-bottom: 20px;
                    opacity: 0.5;
                }
                .empty-text {
                    color: #4a5568;
                    font-size: 18px;
                }
                @keyframes fadeInDown {
                    from { opacity: 0; transform: translateY(-30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💬 Messages</h1>
                    <p class="subtitle">Protected message board</p>
                    <div class="lock-badge">🔐 API Key Required</div>
                </div>
                <div class="action-bar">
                    <div class="message-count">Total Messages: """ + str(len(data_store['messages'])) + """</div>
                    <a href="/" class="back-btn">← Back to Home</a>
                </div>
                <div class="messages-container">
                """ + ("""
                """ + ''.join([f"""
                    <div class="message-card">
                        <div class="message-header">
                            <div class="message-author">
                                <div class="author-avatar">{msg['author'][0].upper()}</div>
                                <div>
                                    <div class="author-name">{msg['author']}</div>
                                    <div class="message-date">{msg['created_at'][:19].replace('T', ' ')}</div>
                                </div>
                            </div>
                        </div>
                        <div class="message-content">{msg['content']}</div>
                    </div>
                """ for msg in reversed(data_store['messages'])]) + """
                """ if data_store['messages'] else """
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <div class="empty-text">No messages yet</div>
                    <p style="color: #718096; margin-top: 10px;">Post your first message using the POST /api/messages endpoint</p>
                </div>
                """) + """
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        message = {
            'id': len(data_store['messages']) + 1,
            'content': data['content'],
            'author': data.get('author', 'Anonymous'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        data_store['messages'].append(message)
        logger.info(f"New message posted by {message['author']}")
        
        return jsonify({
            'message': 'Message posted successfully',
            'data': message
        }), 201

@app.route('/api/search', methods=['GET'])
def search():
    """Search users by name"""
    query = request.args.get('q', '').lower()
    
    if not query:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Search Users</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    color: white;
                    margin-bottom: 50px;
                    animation: fadeInDown 0.6s ease;
                }
                h1 {
                    font-size: 48px;
                    font-weight: 700;
                    margin-bottom: 10px;
                }
                .subtitle {
                    font-size: 18px;
                    opacity: 0.95;
                }
                .search-card {
                    background: rgba(255,255,255,0.95);
                    padding: 50px;
                    border-radius: 24px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                    text-align: center;
                    animation: fadeInUp 0.6s ease 0.2s both;
                }
                .search-icon {
                    font-size: 80px;
                    margin-bottom: 30px;
                }
                .search-form {
                    margin-bottom: 30px;
                }
                .search-input {
                    width: 100%;
                    padding: 18px 25px;
                    font-size: 18px;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    transition: all 0.3s ease;
                    font-family: inherit;
                }
                .search-input:focus {
                    outline: none;
                    border-color: #30cfd0;
                    box-shadow: 0 0 0 3px rgba(48, 207, 208, 0.1);
                }
                .search-btn {
                    width: 100%;
                    margin-top: 15px;
                    padding: 16px;
                    background: linear-gradient(135deg, #30cfd0, #330867);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.3s ease;
                }
                .search-btn:hover {
                    transform: translateY(-2px);
                }
                .info-text {
                    color: #718096;
                    font-size: 14px;
                    margin-bottom: 20px;
                }
                .back-btn {
                    padding: 14px 35px;
                    background: #e2e8f0;
                    color: #2d3748;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 600;
                    display: inline-block;
                    transition: all 0.3s ease;
                }
                .back-btn:hover {
                    background: #cbd5e0;
                    transform: translateY(-2px);
                }
                @keyframes fadeInDown {
                    from { opacity: 0; transform: translateY(-30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 Search Users</h1>
                    <p class="subtitle">Find users by name</p>
                </div>
                <div class="search-card">
                    <div class="search-icon">🔎</div>
                    <form class="search-form" method="GET">
                        <input type="text" name="q" class="search-input" placeholder="Enter user name..." autofocus>
                        <button type="submit" class="search-btn">Search</button>
                    </form>
                    <p class="info-text">Enter a name to search through all registered users</p>
                    <a href="/" class="back-btn">← Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    
    results = [u for u in data_store['users'] if query in u['name'].lower()]
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Results</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 50px;
                animation: fadeInDown 0.6s ease;
            }
            h1 {
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 10px;
            }
            .search-query {
                background: rgba(255,255,255,0.2);
                padding: 8px 20px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 10px;
                backdrop-filter: blur(10px);
            }
            .results-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                animation: fadeInUp 0.6s ease 0.2s both;
            }
            .result-count {
                background: rgba(255,255,255,0.95);
                padding: 12px 25px;
                border-radius: 12px;
                color: #2d3748;
                font-weight: 600;
            }
            .back-btn {
                padding: 12px 30px;
                background: white;
                color: #30cfd0;
                text-decoration: none;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            }
            .results-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 25px;
                animation: fadeInUp 0.6s ease 0.4s both;
            }
            .user-card {
                background: rgba(255,255,255,0.95);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                transition: transform 0.3s ease;
            }
            .user-card:hover {
                transform: translateY(-5px);
            }
            .user-avatar {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #30cfd0, #330867);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 20px;
            }
            .user-name {
                color: #2d3748;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .user-email {
                color: #718096;
                font-size: 14px;
            }
            .empty-state {
                text-align: center;
                padding: 80px 20px;
                background: rgba(255,255,255,0.95);
                border-radius: 20px;
                animation: fadeInUp 0.6s ease 0.4s both;
            }
            .empty-icon {
                font-size: 80px;
                margin-bottom: 20px;
                opacity: 0.5;
            }
            .empty-text {
                color: #4a5568;
                font-size: 18px;
                margin-bottom: 15px;
            }
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Search Results</h1>
                <div class="search-query">Query: """ + query + """</div>
            </div>
            <div class="results-header">
                <div class="result-count">Found """ + str(len(results)) + """ result(s)</div>
                <a href="/api/search" class="back-btn">← New Search</a>
            </div>
            """ + ("""
            <div class="results-grid">
            """ + ''.join([f"""
                <div class="user-card">
                    <div class="user-avatar">{user['name'][0].upper()}</div>
                    <div class="user-name">{user['name']}</div>
                    <div class="user-email">{user['email']}</div>
                </div>
            """ for user in results]) + """
            </div>
            """ if results else """
            <div class="empty-state">
                <div class="empty-icon">😕</div>
                <div class="empty-text">No users found</div>
                <p style="color: #718096;">Try searching with a different name</p>
            </div>
            """) + """
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])