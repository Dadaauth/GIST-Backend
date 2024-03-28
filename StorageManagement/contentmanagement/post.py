from StorageManagement.models.post import Post
from StorageManagement.models.user import User
from utils.verification import verify_kwargs

def create_post(**kwargs) -> tuple:
    """Adds a post made by a user to storage

    Arguments:
        Compulsory:
            user_id: the id of the user making the post

        Optional: (At least 1 of these arguments must be given)
            content: text content of the message
            image: image file of a message
            video: video file of a message
    
    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    verify_kwargs(kwargs, {
        "user_id",
    })
    new_post = Post(
        user_id=kwargs.get('user_id'),
        content=kwargs.get('content'),
        image=kwargs.get('image'),
        video=kwargs.get('video')
    )
    new_post.save() # persist or save the post data to storage
    return True, "The post has been added successfully", 201
    
def get_post(post_id: str) -> tuple:
    """Get a particular post by it's id from the storage
    
    Arguments:
        post_id: the id string of the post to get
    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    post = Post.search(id=post_id)
    if post is None:
        return False, 'Post not found', 404
    return True, post[0].to_dict(), 200

def delete_post(post_id):
    """Deletes a post, referenced by @post_id
    Arguments:
        post_id: the id string of the post to delete

    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    post = Post.search(id=post_id)
    if post is None:
        return False, 'No such post', 404
    post[0].delete()
    return True, "Post deleted successfully", 200

def get_all_posts():
    """Gets all posts from the storage
    Return:
        a tuple. [0]: true or false, [1]: a message to return. [2] possible status code for requests
    """
    posts = Post.all()
    if len(posts) == 0:
        return False, "No posts found", 404
    list_of_posts = []
    for post in posts:
        post = post.to_dict()
        post_owner = User.search(id=post['user_id'])
        if post_owner is None:
            continue
        post['user'] = post_owner[0].to_dict()
        list_of_posts.append(post)
    return True, list_of_posts, 200