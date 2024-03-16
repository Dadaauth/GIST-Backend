from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests

bp = Blueprint('posts', __name__)

storage_service_url = "http://127.0.0.1:5001/api/v1.0/storagemanagement/"
storage_service_url_production = "https://socialnet.clementauthority.me/api/v1.0/storagemanagement/"

@bp.route('/create_post', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    user_id = request.json.get('user_id', None)
    content = request.json.get('content', None)

    if user_id is None:
        return jsonify({'msg': 'A user is required to access this service. No user Id specified'}), 401
    if content is None:
        return jsonify({'msg': 'content is necessary to create a post'}), 400

    response = requests.post(
        f'{storage_service_url}/contentmanagement/create_post',
        json=request.json,
        headers={"Authorization": f"{request.headers.get('Authorization')}"}
    )
    return jsonify(response.json()), 201

@bp.route('/get_post/<post_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_post(post_id):
    response = requests.get(
        f'{storage_service_url}/contentmanagement/get_post/{post_id}',
        headers={"Authorization": f"{request.headers.get('Authorization')}"}
    )
    return jsonify(response.json()), response.status_code

@bp.route('/delete_post/<post_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_post(post_id):
    # TODO: Check if it is the owner of the post that wants to delete the post
    # If not, no permission should be given to delete the post.
    response = requests.delete(
        f"{storage_service_url}/contentmanagement/delete_post/{post_id}",
        headers={"Authorization": f"{request.headers.get('Authorization')}"}
    )
    return jsonify(response.json()), response.status_code

@bp.route('/all_posts', methods=['GET'], strict_slashes=False)
@jwt_required()
def all_posts():
    response = requests.get(
        f'{storage_service_url}/contentmanagement/posts',
        headers={"Authorization": f"{request.headers.get('Authorization')}"}
    )
    return jsonify(response.json()), response.status_code