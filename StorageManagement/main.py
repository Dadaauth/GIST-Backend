from flask import Flask
from flask_jwt_extended import JWTManager, get_jwt, set_access_cookies
from flask_jwt_extended import get_jwt_identity, create_access_token
from datetime import timedelta, timezone, datetime

from models.__init__ import storage1, storage2
from views.usermanagement.main import bp as usermanagement_bp
from views.contentmanagement.main import bp as contentmanagement_bp

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

app.register_blueprint(usermanagement_bp, url_prefix='/api/v1.0/storagemanagement/usermanagement')
app.register_blueprint(contentmanagement_bp, url_prefix='/api/v1.0/storagemanagement/contentmanagement')

@app.route('/api/v1.0/storagemanagement/status')
def status():
    return 'Okay!'


if __name__ == '__main__':
    import os
    import sys

    current_dir = os.getcwd()
    sys.path.append(current_dir)
    app.run(port=5001, debug=True)