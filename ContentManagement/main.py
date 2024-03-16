from flask import Flask, jsonify

from views.posts import bp as posts_bp

app = Flask(__name__)

app.register_blueprint(posts_bp, url_prefix='/api/v1.0/contentmanagement/posts')

@app.route('/api/v1.0/contentmanagement/status', strict_slashes=False)
def status():
    """Return the API status"""
    return jsonify({'status': 'Ok'})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)