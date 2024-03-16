from flask import Flask

from models.__init__ import storage1, storage2
from views.usermanagement.main import bp as usermanagement_bp
from views.contentmanagement.main import bp as contentmanagement_bp

app = Flask(__name__)

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