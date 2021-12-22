from functools import wraps
from flask_login import current_user
from flask import redirect, flash


def login_required_admin(func):
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in and got admin rights before calling the actual view. (If they are
    not, it calls the :attr:`LoginManager.unauthorized` callback.) For
    example::
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.role == 'admin':
            flash('You are not allowed to access this.')
            return redirect('/')
        return func(*args, **kwargs)
    return decorated_view
