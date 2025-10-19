from django.contrib.auth.models import Group, User


GROUP_WEBSITE_ADMINS = 'Website Admins'
GROUP_ACTIVE = 'Active'
GROUP_COMMUNITY_MODS = 'Community Moderators'


def in_group(user: User, group_name: str) -> bool:
    return bool(user and user.is_authenticated and user.groups.filter(name=group_name).exists())
