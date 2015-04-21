USERS = {'editor':'editor',
          'viewer':'viewer',
          'test':'test'}
GROUPS = {'editor':['group:editors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

