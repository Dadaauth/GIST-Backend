def rand_filename(filename, default_ext=None):
    import os
    from uuid import uuid4

    file_ext = os.path.splitext(filename)[1]
    if len(file_ext) == 0:
        # No file extension
        if default_ext is not None:
            file_ext = default_ext
    rand_filename = f"{uuid4()}{file_ext}"
    return rand_filename