def verify_kwargs(kwargs, required_keys):
    """

    :param kwargs: must be a dictionary or set
    :param required_keys: must be a set or dictionary
    :return: true or raise a ValueError if the required keys is not met
    """
    if not all(key in kwargs for key in required_keys):
        raise ValueError(f"Missing required keys: {required_keys - kwargs.keys()}")
    return True

def strip_attrs(obj, attrs: list):
    """Strips an object or dictionary of attributes with sensitive values.
        What will be striped is determined by @attrs

    Arguments:
        obj: the object to work on.
        attrs: a list of attributes to remove from the object.

    Return: The striped object or dictionary if successful else None

    Usage: (doc test)
        >>> from utils.verification import strip_attrs
        >>> an_obj1 = {'username': "clement"}
        >>> an_obj2 = {'username': "clement", "password": "4141clement"}
        >>> strip_attrs(an_obj1, ['password'])
        >>> strip_attrs(an_obj2, ['password'])
        {'username': 'clement'}
    """
    try:
        for attr in attrs:
            if attr in obj:
                del obj[attr]
    except Exception as e:
        return None
    return obj
    

