from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt, set_access_cookies
from flask_jwt_extended import get_jwt_identity, create_access_token
from datetime import timedelta, timezone, datetime

# from models.__init__ import storage1, storage2
from views.usermanagement.user import bp as user_bp
from views.usermanagement.friend import bp as friend_bp
from views.contentmanagement.post import bp as post_bp
from views.contentmanagement.chat import bp as chat_bp

ENV_STATUS = "development"
ENV_SECRET = "asecrethacksectr"

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = ENV_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=48)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_TOKEN_SECURE"] = False if ENV_STATUS == "development" else True
jwt = JWTManager(app)

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

app.register_blueprint(user_bp, url_prefix='/api/v1.0/storagemanagement/usermanagement/user')
app.register_blueprint(friend_bp, url_prefix='/api/v1.0/storagemanagement/usermanagement/friend')
app.register_blueprint(post_bp, url_prefix='/api/v1.0/storagemanagement/contentmanagement/post')
app.register_blueprint(chat_bp, url_prefix='/api/v1.0/storagemanagement/contentmanagement/chat')

@app.route('/api/v1.0/storagemanagement/status')
def status():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    import os
    import sys

    current_dir = os.getcwd()
    sys.path.append(current_dir)
    app.run(port=5001, debug=True)