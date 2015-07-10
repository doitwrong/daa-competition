import os
USERS = {}
GROUPS = {}

users = os.path.join(os.path.dirname(__file__), 'data/users')
permissions = os.path.join(os.path.dirname(__file__), 'data/users_permissions')


def groupfinder(userid, request):
    if userid in get_groups():
        return [get_groups().get(userid, [])]


def get_users():
    with open(users, 'r') as f:
        for line in f:
            (key, val) = line.split()
            USERS[key] = val
    return USERS


def get_groups():
    with open(permissions, 'r') as f:
        for line in f:
            (key, val) = line.split()
            GROUPS[key] = val
    return GROUPS
