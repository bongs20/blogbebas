def role_flags(request):
    user = getattr(request, 'user', None)
    return {
        'is_admin_user': bool(user and user.is_authenticated and user.is_staff),
        'is_superuser': bool(user and user.is_authenticated and user.is_superuser),
    }
