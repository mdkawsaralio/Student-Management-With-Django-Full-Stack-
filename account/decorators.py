from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    def decorator(view):
        @login_required(login_url='login')
        @wraps(view)
        def wrapper(request,*args, **kwargs):
            user=request.user
            
            if user.is_superuser:
                return view(*args, **kwargs)
            if user.groups.filter(name__in=roles).exist():
                return view(*args, **kwargs)
            
            raise PermissionDenied
        return wrapper
    return decorator

def user_in_group(user, group_name):

    if user.is_superuser:
        return True

    return user.groups.filter(name=group_name).exists()