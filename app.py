from flask import Flask
from threading import Thread
import os

app = Flask(__name__)
app.secret_key = 'smartlock_secret_key'

# Import routes from other files
from auth import auth_routes
from lock_control import lock_routes

# Register Blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(lock_routes)

def run_web():
    print("Starting Web Interface...")
    app.run(host='0.0.0.0', port=5000)

def run_detection():
    print("Starting Person Detection...")
    os.system('python3 main.py')

if __name__ == '__main__':
    # Run both processes concurrently
    Thread(target=run_web).start()
    Thread(target=run_detection).start()
