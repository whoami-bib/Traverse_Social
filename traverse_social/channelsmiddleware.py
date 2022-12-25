# # https://stackoverflow.com/questions/65297148/django-channels-jwt-authentication
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
# from channels.middleware import BaseMiddleware
# from channels.auth import AuthMiddlewareStack
# from django.db import close_old_connections
# from urllib.parse import parse_qs
# from jwt import decode as jwt_decode
# from django.conf import settings
# User = settings.AUTH_USER_MODEL

# @database_sync_to_async
# def get_user(validated_token):
#     try:
#         user = User.objects.get(id=validated_token["user_id"])
#         # return get_user_model().objects.get(id=toke_id)
#         print(f"{user}")
#         return user
   
#     except User.DoesNotExist:
#         return AnonymousUser()



# class JwtAuthMiddleware(BaseMiddleware):
#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#        # Close old database connections to prevent usage of timed out connections
#         close_old_connections()

#         # Get the token
#         token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

#         # Try to authenticate the user
#         try:
#             # This will automatically validate the token and raise an error if token is invalid
#             UntypedToken(token)
#         except (InvalidToken, TokenError) as e:
#             # Token is invalid
#             print(e)
#             return None
#         else:
#             #  Then token is valid, decode it
#             decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             print(decoded_data)
#             # Will return a dictionary like -
#             # {
#             #     "token_type": "access",
#             #     "exp": 1568770772,
#             #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
#             #     "user_id": 6
#             # }

#             # Get the user using ID
#             scope["user"] = await get_user(validated_token=decoded_data)
#         return await super().__call__(scope, receive, send)


# def JwtAuthMiddlewareStack(inner):
#     return JwtAuthMiddleware(AuthMiddlewareStack(inner))



from django.conf import settings
User = settings.AUTH_USER_MODEL
# Standard Library
# 

from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async

# import urllib.parse

# @database_sync_to_async
# def get_user(token):
#     try:
#         token = Token.objects.get(key=token)
#         return token.user
#     except Token.DoesNotExist:
#         return AnonymousUser()

# class TokenAuthMiddleware:
#     def __init__(self, inner):
#         self.inner = inner
#     def __call__(self, scope):
#         return TokenAuthMiddlewareInstance(scope, self)


# class TokenAuthMiddlewareInstance:
#     """
#     Yeah, this is black magic:
#     https://github.com/django/channels/issues/1399
#     """
#     def __init__(self, scope, middleware):
#         self.middleware = middleware
#         self.scope = dict(scope)
#         self.inner = self.middleware.inner

#     async def __call__(self, receive, send):
#         decoded_qs = urllib.parse.parse_qs(self.scope["query_string"])
#         if b'token' in decoded_qs:
#           token = decoded_qs.get(b'token').pop().decode()
#           self.scope['user'] = await get_user(token)
#         return await self.inner(self.scope, receive, send)


# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return QueryAuthMiddlewareInstance(scope, self)


class QueryAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        self.scope['user'] = await get_user(int(self.scope["query_string"]))
        inner = self.inner(self.scope)
        return await inner(receive, send)

TokenAuthMiddlewareStack = lambda inner: QueryAuthMiddleware(AuthMiddlewareStack(inner))