# File: app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev"  # Override in production

    @app.route("/")
    def index():
        return "Student Finance Dashboard is running 🚀"
    
    @app.route("/test")
    def test():
        return {"status": "ok", "message": "Test route working!"}

    return app

