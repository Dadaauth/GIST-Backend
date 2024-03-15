def verify_kwargs(kwargs, required_keys):
    """

    :param kwargs: must be a dictionary or set
    :param required_keys: must be a set or dictionary
    :return: true or raise a ValueError if the required keys is not met
    """
    if not all(key in kwargs for key in required_keys):
        raise ValueError(f"Missing required keys: {required_keys - kwargs.keys()}")
    return True
