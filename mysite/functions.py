from django.contrib.auth import login,authenticate
from accounts.models import User
def auto_login(cb):
    def wrap(request,*args,**kwargs):
        if not request.user.is_authenticated:
            user = User.objects.get(username="admin")
            login(request,user)
        return cb(request,*args,**kwargs)
    return wrap