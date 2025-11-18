from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user or not hasattr(current_user, "role"):
                return abort(403)
            if current_user.get_role() not in allowed_roles:
                return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator