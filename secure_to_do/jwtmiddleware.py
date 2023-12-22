import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            try:
                auth_header = headers[b"authorization"].decode()
                token_prefix, token = auth_header.split(" ")
                if token_prefix.lower() == "bearer":
                    decoded_token = jwt.decode(
                        token,
                        options={"verify_signature": True},
                        algorithms=["HS256"],
                    )
                    user_id = decoded_token["user_id"]
                    scope["user"] = await get_user(user_id)
            except (jwt.DecodeError, jwt.InvalidTokenError, KeyError, User.DoesNotExist) as e:
                # Handle exceptions or log the error
                pass

        return await super().__call__(scope, receive, send)