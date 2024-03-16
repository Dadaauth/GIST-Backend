from flask import Blueprint, jsonify, request
from models.Content_Management.post import Post

#TODO: Authenticate all database queries. Authenticate the source making those queries first
# Remember that soeone can easily sniff out information sent between the services so password based authentication
# might not be the best.

bp = Blueprint('contentmanagement_main', __name__)

@bp.route('/create_post', methods=['POST'], strict_slashes=False)
def create_post():
    user_id = request.json.get('email', None)
    content = request.json.get('content', None)
    image_url = request.json.get('image_url', None)
    video_url = request.json.get('video_url', None)
    new_post = Post(
        user_id=user_id,
        content=content,
        image_url=image_url,
        video_url=video_url
    )
    new_post.save()
    return jsonify({'msg': "The post has been added successfully"}), 201
    
@bp.route('/get_post/<post_id>', methods=['GET'], strict_slashes=False)
def get_post(post_id):
    """Get a particular post by it's id from the storage"""
    post = Post.search(id=post_id)
    if post is None:
        return jsonify({'msg': 'Post not found'}), 404
    return jsonify(post[0].to_dict())

@bp.route('/posts', methods=['GET'], strict_slashes=False)
def get_all_posts():
    posts = Post.all()
    if len(posts) == 0:
        return jsonify