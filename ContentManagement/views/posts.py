import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from StorageManagement.contentmanagement import post as post_s
from StorageManagement.contentmanagement import notify as notify_s
from StorageManagement.usermanagement import friend as friend_s

bp = Blueprint('posts', __name__)


@bp.route('/create_post', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    """Creates a new post
    
    Method: POST
    Route: /create_post

    Requirements:
        a logged in user
        form:
            content
        files:
            image, video

    Return: a message depicting the status of the transaction
    """
    user = get_jwt_identity()
    user_id = user['id']
    content = request.form.get('content', None)
    image = request.files.get('image', None)
    video = request.files.get('video', None)

    if user_id is None:
        return jsonify({'msg': 'A user is required to access this service. No user Id specified'}), 401
    if content is None and image is None and video is None:
        return jsonify({'msg': 'No content, image or video passed to create a post. One of these is required'})
    if content is None and image.filename == '' and video.filename == '':
        return jsonify({'msg': 'No content, image or video passed to create a post. One of these is required'})

    response = post_s.create_post(
        user_id=user_id,
        content=content,
        image=image,
        video=video
    )
    if response[0]:
        friends = friend_s.get_friends(user['id'])

        if friends[0]:
            for friend in friends[1]:
                # send a notification to each friend of the user who posted
                notify_s.add_notification(friend.id, "posts", f"{user['first_name']} {user['last_name']} just sent a legendary tale!")

    return jsonify({"msg": response[1]}), response[2]

@bp.route('/get_post/<post_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_post(post_id):
    """Gets a particular post information from storage
    
    Method: GET
    Route: /get_post/<post_id>

    Requirements:
        query parameters or route parameters: post_id
        a logged in user
    
    Return: a jsonified messsage containing the post information
    """
    response = post_s.get_post(post_id)
    return jsonify({"post": response[1]}), response[2]

@bp.route('/delete_post/<post_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_post(post_id):
    """Deletes a post from storage
    
    Method: DELETE
    Route: /delete_post/<post_id>

    Requirements:
        query or route parameters: post_id
        a logged in user

    Return: a status message
    """
    # TODO: Check if it is the owner of the post that wants to delete the post
    # If not, no permission should be given to delete the post.
    response = post_s.delete_post(post_id)
    return jsonify({"msg": response[1]}), response[2]

@bp.route('/all_posts', methods=['GET'], strict_slashes=False)
@jwt_required()
def all_posts():
    """Gets all posts in storage
    
    Method: GET
    Route: /all_posts

    Requirements: none

    Return: a jsonified list of posts
    """
    response = post_s.get_all_posts()
    return jsonify({"posts": response[1]}), response[2]