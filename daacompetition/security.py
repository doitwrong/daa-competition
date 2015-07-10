import os
USERS = {}
GROUPS = {}

users = os.path.join(os.path.dirname(__file__), 'data/users')
permissions = os.path.join(os.path.dirname(__file__), 'data/users_permissions')

with open(users, 'r') as f:
    for line in f:
        (key, val) = line.split()
        USERS[key] = val

with open(permissions, 'r') as f:
    for line in f:
        (key, val) = line.split()
        GROUPS[key] = val

def groupfinder(userid, request):
    print("USERID", userid)
    if userid in get_groups():
        print("DDD#@#@#@#@#@#@#@#@", [get_groups().get(userid, [])])
        return [get_groups().get(userid, [])]


def get_users():
    with open(users, 'r') as f:
        for line in f:
            (key, val) = line.split()
            print('DDDDDDDDDDDDDDDD', key, val)
            USERS[key] = val
    return USERS


def get_groups():
    with open(permissions, 'r') as f:
        for line in f:
            (key, val) = line.split()
            GROUPS[key] = val
    return GROUPS
