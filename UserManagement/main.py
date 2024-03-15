from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from views.auth import bp as auth_bp

# APP NAME `GIST` ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# APP NAME `GIST` ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix='/api/v1.0/usermanagement/auth')

@app.route("/api/v1.0/usermanagement/status", strict_slashes=False)
def status():
    """Return the API status
    """
    return jsonify({"status": "Ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)