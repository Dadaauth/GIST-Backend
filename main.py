import os
from datetime import timedelta, timezone, datetime

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt, set_access_cookies
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from flask_cors import CORS
import socketio
from dotenv import load_dotenv

from UserManagement.main import bp as usermanagement_bp
from ContentManagement.main import bp as contentmanagement_bp
from ChatNotificationFeed.main import bp as chatnotificationfeed_bp

# APP NAME `GIST` ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# APP NAME `GIST` ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

load_dotenv()
enviroment = os.environ.get("ENV")

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config['ENV'] = enviroment
    app.config['SESSION_COOKIE_SECURE'] = True if enviroment == "production" else False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=48)
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_TOKEN_SECURE"] = True if enviroment == "production" else False
    app.config['JWT_REFRESH_DELTA'] = timedelta(days=7)
    jwt = JWTManager(app)

    sio = socketio.Server()
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    app.sio = sio

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the response
            return response


    app.register_blueprint(usermanagement_bp, url_prefix="/api/v1.0/usermanagement")
    app.register_blueprint(contentmanagement_bp, url_prefix="/api/v1.0/contentmanagement")
    app.register_blueprint(chatnotificationfeed_bp, url_prefix="/api/v1.0/chatnotificationfeed")

    # @app.route("/api/v1.0/static/<file_name>", strict_slashes=False)
    # @jwt_required()
    # def status():
    #     pass


    @app.route("/api/v1.0/status/", strict_slashes=False)
    def status():
        """Returns the status of our API"""
        return jsonify({"status": "ok"})

    return app

app = create_app()
if __name__ == "__main__":
    import os
    import sys

    current_dir = os.getcwd()
    sys.path.append(current_dir)
    app.run(host="127.0.0.1", port=5000, debug=True)