from StorageManagement.models.notify import Notify


def add_notification(user_id: str, type: str, content: str) -> tuple:
    """Adds a notification for a user to the storage system

    Arguments:
        user_id: the id of the user to receive the notification.
        type: string, the type of notification being sent. Could be "posts", "friend requests", "calls" or "messages"
        content: the message or content of the notification. What to display.
    
    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    try:
        notify = Notify(user_id=user_id, type=type, content=content)
        notify.save()
    except ValueError:
        return False, """
            A value error was raised. Most likely
            a mistake with the value of type sent to notification system
            """ , 400
    return True, "Notification saved successfully", 201

def get_notifications(user_id):
    """Get notifications for a particular user based on @user_id

    Arguments:
        user_id: the id of the user whose notification is needed
    
    Return:
        a tuple. [0]: true or false, [1]: list of notifications to return. [2] possible status code for requests
    """
    notifys = Notify.search(user_id=user_id)
    if notifys is None:
        return False, "No notifications found for the current user", 404
    
    list_of_notifys = []
    for notify in notifys:
        list_of_notifys.append(notify.to_dict())

    return True, list_of_notifys, 200