from .utils import in_group, GROUP_WEBSITE_ADMINS


def role_flags(request):
    user = getattr(request, 'user', None)
    return {
    'is_admin_user': bool(user and in_group(user, GROUP_WEBSITE_ADMINS)),
        'is_superuser': bool(user and user.is_authenticated and user.is_superuser),
    }
