from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth  # Import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

# Switch between authentication mechanisms
auth_type = getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()

@app.before_request
def before_request() -> None:
    """ Before request handler """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth.require_auth(request.path, excluded_paths):
        if not auth.authorization_header(request):
            abort(401)
        user = auth.current_user(request)
        if user is None:
            abort(403)
        request.current_user = user

@app.teardown_appcontext
def teardown_db(exception):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
