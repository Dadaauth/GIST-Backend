from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.ChatNotificationFeed.notify import Notify

bp = Blueprint("notify", __name__)

@bp.route("/add_notification", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_notification():
    user_id = request.json.get('user_id')
    type = request.json.get("type")
    content = request.json.get("content")
    try:
        notify = Notify(user_id=user_id, type=type, content=content)
        notify.save()
    except ValueError:
        return jsonify({
            "msg": "A value error was raised. Most likely a mistake" \
            "with the value of type sent to notification system"
        }), 400
    return jsonify({"msg": "Notification saved successfully"}), 201

@bp.route('/get_notifications', methods=["GET"], strict_slashes=False)
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()['id']
    notifys = Notify.search(user_id=user_id)
    if notifys is None:
        return jsonify({"msg": "No notifications found for the current user"}), 404
    
    list_of_notifys = []
    for notify in notifys:
        list_of_notifys.append(notify.to_dict())

    return jsonify(list_of_notifys), 200