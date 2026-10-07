from .decorators import user_in_group


def user_roles(request):

    if not request.user.is_authenticated:
        return {
            'is_admin': False,
            'is_teacher': False,
            'is_student': False,
        }

    return {
        'is_admin': user_in_group(request.user, 'Admin'),
        'is_teacher': user_in_group(request.user, 'Teacher'),
        'is_student': user_in_group(request.user, 'Student'),
    }