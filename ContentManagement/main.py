from flask import Flask, jsonify

app = Flask(__name__)



@app.route('/api/v1.0/contentmanagement/status', strict_slashes=False)
def status():
    """Return the API status"""
    return jsonify({'status': 'Ok'})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)