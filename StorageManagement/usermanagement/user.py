from StorageManagement.models.user import User
from StorageManagement.models.friend import Friend
from utils.verification import verify_kwargs, strip_attrs
from .friend import get_friends

def create_user(**kwargs):
    """Creates a new user in storage
    
    Arguments:
        email: the email to assign the new user,
        first_name: the first name of the new user
        last_name: the last_name of the new user.
        password: the password of the new user.

        Optional:
            profile_pic: the profile picture of the new user. It should be a file instance|object

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests

    Usage: (doc test)
        # >>> import this
    """
    verify_kwargs(kwargs, {
        "email",
        "first_name",
        "last_name",
        "password",
    })
    email = kwargs.get('email', None)
    first_name = kwargs.get('first_name', None)
    last_name = kwargs.get('last_name', None)
    password = kwargs.get('password', None)
    profile_pic = kwargs.get('profile_pic', None)
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        profile_pic=profile_pic,
        password=password
    )
    new_user.save()
    return True, "A new user has been created successfully", 201

def get_user(user_id):
    """Get a single user information based on an @user_id
    
    Argument:
        user_id: the id of the user whose information is needed

    Return:
        a tuple. [0]: true or false, [1]: the user dictionary. [2] possible status code for requests

    Usage: (doc test)
        >>> .user import get_user
        >>> user = get_user('b93c6b74-afbe-46b0-ba5d-96ebea4a1fc0')
        >>> print(user)
    """
    user = User.search(id=user_id)
    if user is None:
        return False, "User not found", 404
    user_stripped = strip_attrs(user[0].to_dict(), ['password'])
    return True, user_stripped, 200

def get_user_by_email(user_email):
    """ Get a particular user based on their email
    Arguments:
        email: the email of the user whose information is needed
    
    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests

    Usage: (doc test)
        # >>> import this
    """
    user = User.search(email=user_email)
    if user is None:
        return False, "User not found", 404
    user_stripped = strip_attrs(user[0].to_dict(), ['password'])
    return True, user_stripped, 200

def get_all_users(redact=True):
    """Get all users in storage, yes I mean all....

    Arguments:
        redact (Default True), if True, sensitive information like password will be removed from the user information
    
    Return:
        a tuple. [0]: true or false, [1]: a list of users or a message if an error occurs. [2] possible status code for requests
    """
    users = User.all()
    if len(users) == 0:
        return False, "No users found", 404
    list_of_users = []
    for user in users:
        if redact:
            # Remove sensitive information if redact is specified as True
            user_stripped = strip_attrs(user.to_dict(), ['password'])
            list_of_users.append(user_stripped)
        else:
            list_of_users.append(user.to_dict())
    return True, list_of_users, 200

# def get_friends(user_id):
#     """Gets all the friends a user has in storage.

#     Diff: The get_friends function in the friends page gets each user information
#             after fetching the friends a user has. This function only returns the
#             friends table without the actual users information.

#     Requirements: user_id

#     Return: a tuple [0] true or false, [1] a list of friends or error message, [2] a possible status code
#     """
#     no_friends = False
#     list_of_friends = []

#     friends = Friend.search(user_id=user_id, status="friends")
#     if friends is None:
#         no_friends = True
#     else:
#         for friend in friends:
#             list_of_friends.append(friend)

#     # Check for friends in the other way round with friend_id=user_id
#     # due to the way they are stored in storage during friend requests
#     friends = Friend.search(friend_id=user_id, status="friends")
#     if friends is None and no_friends:
#         False, 'No friends found', 404
#     elif friends is not None:
#         for friend in friends:
#             list_of_friends.append(friend)

#     return True, list_of_friends, 200

def get_non_friends(user_id):
    """Get users in storage that are not part of the logged in user friends.
    
    Return:
        a tuple. [0]: true or false, [1]: a list of users or a message if an error occurs. [2] possible status code for requests
    """
    users = User.all()
    friends = get_friends(user_id)[1]
    if len(users) == 0:
        return False, "No users found", 404
    list_of_users = []
    is_a_friend = False
    for user in users:
        if friends is not None:
            for friend in friends:
                print(friend)
                if user.id == friend['id']:
                    is_a_friend = True
        if is_a_friend:
            is_a_friend = False
            continue
        user_stripped = strip_attrs(user.to_dict(), ['password'])
        list_of_users.append(user_stripped)
    return True, list_of_users, 200
