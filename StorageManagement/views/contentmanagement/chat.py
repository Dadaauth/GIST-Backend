from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models.ChatNotificationFeed.message import Message
from models.ChatNotificationFeed.conversation import Conversation, ConversationParticipants
from models.User_Management.user import User

bp = Blueprint('chat', __name__)

@bp.route('/create_message', methods=["POST"], strict_slashes=False)
@jwt_required()
def create_message():
    sender_id = request.form.get('sender_id')
    conversation_id = request.form.get('conversation_id')
    content = request.form.get('content')
    image = request.files.get('image', None)
    video = request.files.get('video', None)
    if sender_id is None or conversation_id is None:
        return jsonify({'msg': 'sender_id or conversation_id not passed'}), 400

    # check if the sender is in the conversation
    sender_in_conversation = False
    conv_participants = ConversationParticipants.search(conversation_id=conversation_id)
    if conv_participants is not None:
        for conv_part in conv_participants:
            conv_part = conv_part.to_dict()
            if sender_id == conv_part["user_id"]:
                sender_in_conversation = True

    if not sender_in_conversation:
        return jsonify({"msg": "This sender id can't be found among the conversation participants"}), 400
    
    new_message = Message(
        sender_id=sender_id,
        conversation_id=conversation_id,
        content=content,
        image=image,
        video=video
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

@bp.route('/get_conversation/<conv_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_conversation(conv_id):
    conversation = Conversation.search(id=conv_id)
    messages = Message.search(conversation_id=conv_id)
    conv_participants = ConversationParticipants.search(conversation_id=conv_id)
    tmp = []

    if conversation is None:
        return jsonify({"msg": "No conversation matched conversation_id in storage"}), 400
    else:
        conversation = conversation[0].to_dict()
    if conv_participants is None:
        return jsonify({'msg': "error, conversation participants not found in this conversation"}), 404
    
    for message in messages:
        tmp.append(message.to_dict())
    messages = tmp
    # sort the messages based on the time
    messages = sorted(messages, key=lambda message: message['send_time'])
    tmp = []
    for conv_participant in conv_participants:
        user = User.search(id=conv_participant.user_id)
        if user is None:
            continue
        tmp.append(user[0].to_dict())
    conv_participants = tmp

    return jsonify({
        "msg": "conversation gotten successfully",
        "conversation": conversation,
        "messages": messages,
        "conversation_participants": conv_participants
    }), 200