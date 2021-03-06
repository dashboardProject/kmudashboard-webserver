import webapp2

from functools import wraps
from database_Model import GroupMap
from google.appengine.api import users
from utils.userNgroupQuery import selectUser, selectUsersInGroup, selectGroupsOfUser

def userCheck(func):

    @wraps(func)
    def decorated_function(self, *args):
        user = users.get_current_user()

        # check google account
        if user:
            # check app account
            if selectUser(user.email()).count() is 0:
                return webapp2.redirect_to('signup')

            else:
                if len(args) > 0:
                    email = user.email()
                    gid = int(args[0])
                    if selectGroupsOfUser(email).filter(GroupMap.groupId == gid).count() is 0:
                        return webapp2.redirect_to('main')

                return func(self, *args)

        # not sign-in google account yet
        else:
            return webapp2.redirect(users.create_login_url(self.request.uri))

    return decorated_function