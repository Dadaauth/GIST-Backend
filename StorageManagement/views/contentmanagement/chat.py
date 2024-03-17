from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models.ChatNotificationFeed.message import Message
from models.ChatNotificationFeed.conversation import Conversation, ConversationParticipants

bp = Blueprint('chat', __name__)

@bp.route('/create_message', methods=["POST"], strict_slashes=False)
@jwt_required()
def create_message():
    sender_id = request.json.get('sender_id')
    conversation_id = request.json.get('conversation_id')
    content = request.json.get('content', None)
    image_url = request.json.get('image_url', None)
    video_url = request.json.get('video_url', None)
    if sender_id is None or conversation_id is None:
        return jsonify({'msg': 'sender_id or conversation_id not passed'}), 400

    new_message = Message(
        sender_id=sender_id,
        conversation_id=conversation_id,
        content=content,
        image_url=image_url,
        video_url=video_url
    )
    new_message.save()
    return jsonify({'msg': "new message saved successfully"}), 201

@bp.route('/create_conversation', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_conversation():
    conv_name = request.json.get('name', None)
    # conv_particiants should be sent as a list inside a json
    conv_participants = request.json.get('participants', None)

    if conv_name is None:
        return jsonify({'msg': 'conversation name is not given'}), 400
    if conv_participants is None or len(conv_participants) < 2:
        return jsonify({'msg': 'conversation participant cannot be less than 2'}), 400
    
    # TODO: confirm that all conversation participants
    # sent are actual users in storage.

    new_conversation = Conversation(conv_name)
    new_conversation.save()

    for conv_participant in conv_participants:
        new_conv_part = ConversationParticipants(conv_participant, new_conversation.id)
        new_conv_part.save()

    return jsonify({
        'msg': 'new conversation created successfully, participants added.',
        'conversation_id': new_conversation.id
    }), 201