from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.User_Management.friend import Friend
from models.User_Management.user import User

bp = Blueprint('friend', __name__)

@bp.route('/add_friend', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_friend():
    user_id = get_jwt_identity()['id']
    friend_id = request.json.get('friend_id', None)
    
    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    
    friend = Friend(
        user_id=user_id,
        friend_id=friend_id,
        status="pending"
    )
    friend.save()

    return jsonify({"msg": "The friend has been added successfully"}), 201

@bp.route('/accept_friend', methods=['POST'], strict_slashes=False)
@jwt_required()
def accept_friend():
    user_id = get_jwt_identity()['id']
    friend_id = request.json.get('friend_id', None)
    
    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    
    friend = Friend.search(user_id=friend_id, friend_id=user_id)
    if friend is None:
        return jsonify({'msg': 'Friend request not found'}), 404
    
    if friend[0].status == "pending":
        friend[0].status = "friends"
        friend[0].save()

    return jsonify({"msg": "The friend has been accepted successfully"}), 201

@bp.route('/reject_friend_request', methods=['POST'], strict_slashes=False)
@jwt_required()
def reject_friend_request():
    user_id = get_jwt_identity()['id']
    friend_id = request.json.get('friend_id', None)
    
    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    
    friend = Friend.search(user_id=friend_id, friend_id=user_id)
    if friend is None:
        return jsonify({'msg': 'Friend not found'}), 404
    friend[0].delete()

    return jsonify({"msg": "The friend has been removed successfully"}), 201

@bp.route('/friends', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friends():
    no_friends = False
    user_id = get_jwt_identity()['id']

    friends = Friend.search(user_id=user_id, status="friends")
    if friends is None:
        no_friends = True

    list_of_friends = []
    for friend in friends:
        user = User.search(id=friend.id)
        if user is not None:
            list_of_friends.append(user.to_dict())

    friends = Friend.search(friend_id=user_id, status="Friends")
    if friends is None and no_friends:
        return jsonify({'msg': 'No friends found'}), 404
    else:
        for friend in friends:
            list_of_friends.append(friend.to_dict())

    return jsonify(list_of_friends), 200

@bp.route('/friend_requests', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friend_requests():
    user_id = get_jwt_identity()['id']
    friend_requests = Friend.search(friend_id=user_id, status="pending")
    if friend_requests is None:
        return jsonify({'msg': 'No friend requests found'}), 404
    list_of_friend_requests = []
    for friend_request in friend_requests:
        list_of_friend_requests.append(friend_request.to_dict())
    return jsonify(list_of_friend_requests), 200

@bp.route('/sent_friend_requests', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_sent_friend_requests():
    user_id = get_jwt_identity()['id']
    sent_friend_requests = Friend.search(user_id=user_id, status="pending")
    if sent_friend_requests is None:
        return jsonify({'msg': 'No sent friend requests found'}), 404
    list_of_sent_friend_requests = []
    for sent_friend_request in sent_friend_requests:
        list_of_sent_friend_requests.append(sent_friend_request.to_dict())
    return jsonify(list_of_sent_friend_requests), 200

@bp.route('/friend/<friend_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friend(friend_id):
    user_id = get_jwt_identity()['id']
    friend = Friend.search(user_id=user_id, friend_id=friend_id)
    if friend is None:
        friend = Friend.search(user_id=friend_id, friend_id=user_id)
        if friend is None:
            return jsonify({'msg': 'Friend not found'}), 404

    return jsonify(friend[0].to_dict()), 200

@bp.route('/block/<friend_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def block_friend(friend_id):
    user_id = get_jwt_identity()['id']
    friend = Friend.search(user_id=user_id, friend_id=friend_id)
    
    if friend is None:
        friend = Friend.search(friend_id=user_id, user_id=friend_id)
        if friend is None:
            return jsonify({'msg': 'Friend not found'}), 404
    
    if friend[0].status == "friends":
        friend[0].status = "blocked"
        friend[0].save()

    return jsonify({"msg": "The friend has been blocked successfully"}), 201