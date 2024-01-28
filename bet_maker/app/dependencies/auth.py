import fastapi
import httpx
from bet_maker.core.config import settings
from fastapi import Header


class AuthRequired:

    @classmethod
    async def handle(cls, access_token: str = Header()):
        response = httpx.get(
            url=settings.get_user_route,
            headers={"token": access_token.encode("utf-8")}
        )
        if response.status_code != 200:
            raise fastapi.HTTPException(
                fastapi.status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        return response.json()
