from flask import Flask
from config import Config
from database import init_db

app = Flask(__name__)
app.config.from_object(Config)

init_db()

from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)