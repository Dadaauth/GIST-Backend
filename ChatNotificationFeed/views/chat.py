from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests

bp = Blueprint('chat', __name__)

storage_service_url = "http://127.0.0.1:5001/api/v1.0/storagemanagement/"
storage_service_url_production = "https://socialnet.clementauthority.me/api/v1.0/storagemanagement/"


@bp.route('/create_message', method=["POST"], strict_slashes=False)
@jwt_required()
def create_message():
    sender_id = request.json.get('sender_id')
    conversation_id = request.json.get('conversation_id')
    content = request.json.get('content', None)
    image_url = request.json.get('image_url', None)
    video_url = request.json.get('video_url', None)

    # Check that the sender_id belongs to an actual user
    # in storage

    response = requests.post(
        f"{storage_service_url}/contentmanagement/chat/create_message",
        json={
            "sender_id": sender_id,
            "conversation_id": conversation_id,
            "content": content,
            "image_url": image_url,
            "video_url": video_url
        }
    )
    return jsonify(response.json()), response.status_code

@bp.route('/create_conversation', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_conversation():
    name = request.json.get('name', None)
    participants = request.json.get('participants', None)
    response = requests.post(
        f'{storage_service_url}/contentmanagement/chat/create_conversation',
        json={
            "name": name,
            "participants": participants
        }
    )
    return jsonify(response.json()), response.status_code