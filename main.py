from flask import Flask, jsonify


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route("/api/v1/status/", strict_slashes=False)
def status():
    """Returns the status of our API"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=5000, debug=True)