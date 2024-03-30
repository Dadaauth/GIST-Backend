import os

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from StorageManagement.contentmanagement import chat as chat_s

bp = Blueprint('chat', __name__)

@bp.route('/create_message', methods=["POST"], strict_slashes=False)
@jwt_required()
def create_message():
    """Sends a new message to another user or to a conversation room
    
    Method: POST
    Route: /create_message

    Requirements:
        a logged in user
        form:
            sender_id, conversation_id, content
        files:
            image, video
    Return: A status message
    """
    sender_id = request.form.get('sender_id', None)
    conversation_id = request.form.get('conversation_id')
    content = request.form.get('message', None)
    image = request.files.get('image', None)
    video = request.files.get('video', None)

    print(request.form)
    if sender_id is None:
        sender_id = get_jwt_identity()['id']

    # Check that the sender_id belongs to an actual user
    # in storage
    response = chat_s.create_message(
        sender_id=sender_id,
        conversation_id=conversation_id,
        content=content,
        image=image,
        video=video
    )
    return response[1], response[2]

@bp.route('/create_conversation', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_conversation():
    """Creates a conversation between user
    
    Method: POST
    Route: /create_conversation

    Requirements:
        json:
            name, participants(list)

    Return: a status message
    """
    name = request.json.get('name', None)
    participants = request.json.get('participants', None)

    if len(participants) == 1:
        participants.append(get_jwt_identity()['id'])
    response = chat_s.create_conversation(name, participants)
    return response[1], response[2]

@bp.route('/get_conversation/<conv_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_conversation(conv_id):
    """Gets details about a particular conversation
    
    Method: GET
    Route: /get_conversation/<conv_id>

    Requirements:
        query or route params:
            conv_id
    Return:  a json/object representation of the conversation gotten or an error message
    """
    response = chat_s.get_conversation(conv_id)
    return response[1], response[2]