import fastapi
import jwt
import tortoise.exceptions
from fastapi import Header
from accounts.models import User
from accounts.config import settings


class JwtValidator:

    @classmethod
    def validate(cls, token: bytes):
        try:
            token_dict = jwt.decode(token, algorithms=settings.algorithm, key=settings.secret)
        except (AttributeError, jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError, jwt.exceptions.ExpiredSignatureError) as e:
            raise e
        else:
            return token_dict.get("email")


class UserManager:

    @classmethod
    async def get_user(cls, token: bytes | None = Header()):
        jwt_validator = JwtValidator()
        try:
            email = jwt_validator.validate(token)
        except (AttributeError, jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError) as e:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        try:
            user = await User.get(email=email)
        except tortoise.exceptions.DoesNotExist:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        else:
            return user
