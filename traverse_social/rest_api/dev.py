from django.contrib.auth import get_user_model
from rest_framework import authentication


User = get_user_model

class DevAuthentication(authentication.BasicAuthentication):

    def authenticate(self, request):
        print("______________________dfsadfdfsdf")
        qs = User.objects.filter(id = 1)
        user = qs.order_by('?').first()

        print(user)

        return (user, None)