import os
USERS = {}
GROUPS = {}

users = os.path.join(os.path.dirname(__file__), 'data/users')
permissions = os.path.join(os.path.dirname(__file__), 'data/users_permissions')

with open(users) as f:
    for line in f:
       (key, val) = line.split()
       USERS[key] = val

with open(permissions) as f:
    for line in f:
        (key, val) = line.split()
        GROUPS[key] = val

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
