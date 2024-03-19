from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from models.Content_Management.post import Post

#TODO: Authenticate all database queries. Authenticate the source making those queries first
# Remember that soeone can easily sniff out information sent between the services so password based authentication
# might not be the best.

bp = Blueprint('post', __name__)

@bp.route('/create_post', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    user_id = request.form.get('user_id', None)
    content = request.form.get('content', None)
    image = request.files.get('image', None)
    video = request.files.get('video', None)
    new_post = Post(
        user_id=user_id,
        content=content,
        image=image,
        video=video
    )
    new_post.save()
    return jsonify({"msg": "The post has been added successfully"}), 201
    
@bp.route('/get_post/<post_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_post(post_id):
    """Get a particular post by it's id from the storage"""
    post = Post.search(id=post_id)
    if post is None:
        return jsonify({'msg': 'Post not found'}), 404
    return jsonify(post[0].to_dict())

@bp.route('/delete_post/<post_id>', methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_post(post_id):
    post = Post.search(id=post_id)
    if post is None:
        return jsonify({'msg': 'No such post'}), 404
    post[0].delete()
    return jsonify({"msg": "Post deleted successfully"}), 200

@bp.route('/posts', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_posts():
    posts = Post.all()
    if len(posts) == 0:
        return jsonify({'msg': "No posts found"}), 404
    list_of_posts = []
    for post in posts:
        list_of_posts.append(post.to_dict())
    return jsonify(list_of_posts), 200