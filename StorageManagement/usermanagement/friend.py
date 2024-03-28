from StorageManagement.models.friend import Friend
from StorageManagement.models.user import User
from utils.verification import strip_attrs


def add_friend(user_id: str, friend_id: str) -> tuple:
    """Add a friendship row to the database. Connects two users together.
        The connection status is 'pending' in this function, call accept_friend
        to accept the friendship from the other user's side and change the status to 'friends'

    Arguments:
        user_id: the id of the user seeking a friend request
        friend_id: the id of the lucky guy or lady

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    if friend_id is None or user_id is None:
        return False, 'required parameter(s) not present', 400
    
    friend = Friend(
        user_id=user_id,
        friend_id=friend_id,
        status="pending"
    )
    friend.save()

    return True, "The friend has been added successfully", 201

def accept_friend(user_id: str, friend_id: str) -> tuple:
    """
    Accept a friend request hereby changing the status to 'friends'

    Arguments:
        user_id: The id of the user to accept the friend request
        friend_id: the id of the friend who sent the friend request.

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests

    Usage: (doctest)
        # >>> import this
        >>>
    """
    
    if friend_id is None or user_id is None:
        return False, 'friend_id or user_id is not present in request', 400
    
    friend = Friend.search(user_id=friend_id, friend_id=user_id)
    if friend is None:
        return False, 'Friend request not found', 404
    
    if friend[0].status == "pending":
        friend[0].status = "friends"
        friend[0].save()

    return True, "The friend request has been accepted successfully", 201

def reject_friend_request(user_id: str, friend_id: str) -> tuple:
    """Rejects a friend request and deletes the friend request from the storage

    Arguments:
        user_id: the id of the user receiving and rejecting the friends request.
        friend_id: the id of the user who sent the friend request.

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests

    Usage: (doc test)
        # >>> import this
    """
    
    if friend_id is None or user_id is None:
        return False, 'friend_id or user_id is not present in request', 400
    
    friend = Friend.search(user_id=friend_id, friend_id=user_id)
    if friend is None:
        return False, 'Friend not found', 404
    friend[0].delete()

    return True, "The friend has been removed successfully", 201

def get_friends(user_id):
    """Get all the friends of a particular user based on @user_id

    Arguments:
        user_id: the id of the user whose records are needed

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests

    Usage: (doc test)
        >>> from StorageManagement.usermanagement.friend import get_friends
        >>> get_friends(123)
        (True, [], 200)

    """
    no_friends = False
    list_of_friends = []

    friends = Friend.search(user_id=user_id, status="friends")
    if friends is None:
        no_friends = True
    else:
        for friend in friends:
            user = User.search(id=friend.friend_id)
            if user is not None:
                user = user[0]
                user_striped = strip_attrs(user.to_dict(), ['password']) # remove password fom the user object before returning
                if user_striped is None:
                    raise Exception('Error in striping user object of sensitive values')
                list_of_friends.append(user_striped)

    # Check for friends in the other way round with friend_id=user_id
    # due to the way they are stored in storage during friend requests
    friends = Friend.search(friend_id=user_id, status="friends")
    if friends is None and no_friends:
        False, 'No friends found', 404
    elif friends is not None:
        for friend in friends:
            user = User.search(id=friend.user_id)
            if user is not None:
                user = user[0]
                user_striped = strip_attrs(user.to_dict(), ['password']) # remove password fom the user object before returning
                if user_striped is None:
                    raise Exception('Error in striping user object of sensitive values')
                list_of_friends.append(user_striped)

    return True, list_of_friends, 200

def get_friend_requests(user_id: str):
    """Gets all friend requests sent to a particular user
    
    Arguments:
        user_id: the is of the user whose information is needed

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests

    Usage: (doc test)
        # >>> import this
    """
    friend_requests = Friend.search(friend_id=user_id, status="pending")
    if friend_requests is None:
        return False, 'No friend requests found', 404
    
    list_of_friend_requests = []
    for friend_req in friend_requests:
        user = User.search(id=friend_req.user_id)[0]
        if user is not None:
            user_striped = strip_attrs(user.to_dict(), ['password']) # remove password fom the user object before returning
            if user_striped is None:
                raise Exception('Error in striping user object of sensitive values')
            list_of_friend_requests.append(user_striped)
    return True, list_of_friend_requests, 200

def get_sent_friend_requests(user_id: str):
    """Gets the friend requests a particular user has sent out but is not accepted yet.
    
    Arguments: user_id => The id of the user whose information is needed

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    
    Usage: (doc test)
        # >>> import this
    """
    sent_friend_requests = Friend.search(user_id=user_id, status="pending")
    if sent_friend_requests is None:
        return False, 'No sent friend requests found', 404
    list_of_sent_friend_requests = []
    for sent_friend_request in sent_friend_requests:
        list_of_sent_friend_requests.append(sent_friend_request.to_dict())
    return True, list_of_sent_friend_requests, 200

# def get_friend(friend_id):
#     user_id = get_jwt_identity()['id']
#     friend = Friend.search(user_id=user_id, friend_id=friend_id)
#     if friend is None:
#         friend = Friend.search(user_id=friend_id, friend_id=user_id)
#         if friend is None:
#             return jsonify({'msg': 'Friend not found'}), 404

#     return jsonify(friend[0].to_dict()), 200

def block_friend(user_id, friend_id):
    """Block a particular friend specified by @friend_id
    
    Arguments:
        user_id: the user trying to block a friend
        friend_id: The unlucky friend being blocked

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    friend = Friend.search(user_id=user_id, friend_id=friend_id)
    
    if friend is None:
        friend = Friend.search(friend_id=user_id, user_id=friend_id)
        if friend is None:
            return False, 'Friend not found', 404
    
    if friend[0].status == "friends":
        friend[0].status = "blocked"
        friend[0].save()

    return True, "The friend has been blocked successfully", 201