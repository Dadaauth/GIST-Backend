from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

bp = Blueprint('posts', __name__)

storage_service_url = "http://127.0.0.1:5001/api/v1.0/storagemanagement/"
storage_service_url_production = "https://socialnet.clementauthority.me/api/v1.0/storagemanagement/"

@bp.route('/create_post', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    user_id = request.form.get('user_id', None)
    content = request.form.get('user_id', None)
    image = request.files.get('image', None)
    video = request.files.get('video', None)

    if user_id is None:
        return jsonify({'msg': 'A user is required to access this service. No user Id specified'}), 401
    if content is None and image is None and video is None:
        return jsonify({'msg': 'No content, image or video passed to create a post. One of these is required'})
    if content is None and image.filename == '' and video.filename == '':
        return jsonify({'msg': 'No content, image or video passed to create a post. One of these is required'})

    response = requests.post(
        f'{storage_service_url}/contentmanagement/create_post',
        data=request.form,
        files=request.files,
        headers={"Authorization": f"{request.headers.get('Authorization')}"}
    )
    if response.status_code not in {400, 404, 500, 501}:
        # send a notification to each friend of the user who posted
        friends = requests.get(f"{storage_service_url}/usermanagement/friend/friends")
        if friends.status_code == 200:
            user = get_jwt_identity()
            for friend in friends.json():
                requests.post(
                    f"{storage_service_url}/contentmanagement/notify/add_notification",
                    json={
                        "user_id": friend.id,
                        "type": "posts",
                        "content": f"{user['first_name']} {user['last_name']} just sent a legendary tale!"
                    },
                    headers={"Authorization": request.headers.get('Authorization')}
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