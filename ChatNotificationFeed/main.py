from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt, set_access_cookies
from flask_jwt_extended import get_jwt_identity, create_access_token
from datetime import timedelta, timezone, datetime

from views.chat import bp as chat_bp

ENV_STATUS = "development"
ENV_SECRET = "asecrethacksectr"

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = ENV_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=48)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_TOKEN_SECURE"] = False if ENV_STATUS == "development" else True
jwt = JWTManager(app)

#TODO: JWT should get its tokens from the database for the sake of the other services

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

app.register_blueprint(chat_bp, url_prefix='/api/v1.0/chatnotificationfeed/chat')

@app.route("/api/v1.0/chatnotificationfeed/status", strict_slashes=False)
def status():
    """Return the status of the API
    """
    return jsonify({"status": "Ok"})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5003, debug=True)