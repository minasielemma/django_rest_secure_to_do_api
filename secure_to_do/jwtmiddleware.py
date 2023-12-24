from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.exceptions import DenyConnection

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
        self.jwt_auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        token = scope['query_string'].decode().split('=')[1]
        try:
            access_token = AccessToken(token)
            user = await get_user(access_token['user_id'])
            if user is not None:
                scope['user'] = user
                scope['user_id'] = user.id
            else:
                raise DenyConnection("Invalid token or user not found.")
        except Exception as e:
            raise DenyConnection("Invalid token or user not found.")

        return await self.inner(scope, receive, send)