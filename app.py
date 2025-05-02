import os  # For accessing environment variables
from flask import Flask, jsonify, request, Response
from functools import wraps
from dotenv import load_dotenv  # To load variables from .env file

# Load the .env file
load_dotenv()

app = Flask(__name__)

# Get credentials from environment variables
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Function to validate credentials
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# If authentication fails, send a 401 response
def authenticate():
    return Response(
        'Could not verify your access level.\n'
        'Please provide valid credentials.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Decorator to protect routes
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Example public route
@app.route('/')
def home():
    return 'Welcome, Project William!'

# Protected route
@app.route('/data')
@requires_auth
def data():
    sample_data = {
        'user': 'Client A',
        'clicks': 124,
        'impressions': 5230,
        'conversions': 14,
        'conversion_rate': '1.92%'
    }
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(debug=True)
