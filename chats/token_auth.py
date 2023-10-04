from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
import asyncio
import jwt, re
from django.conf import LazySettings
settings = LazySettings()
from channels.db import database_sync_to_async
from api_auth.models import User
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
import traceback


@database_sync_to_async
def get_user(user_jwt):
    try:
        return User.objects.get(id=user_jwt)
    except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
        return AnonymousUser()
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        try: 
            query_string = parse_qs(self.scope["query_string"].decode("utf8"))
            if 'bearer' in query_string:
                token_key = query_string['bearer']
                user_jwt = jwt.decode(
                            token_key[0],
                            settings.SECRET_KEY,
                        )
                id = user_jwt['user_id']
                self.scope['user'] = await get_user(id)
        except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
            self.scope['user'] =  AnonymousUser()
        inner = self.inner(self.scope)
        return await inner(receive, send) 

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
