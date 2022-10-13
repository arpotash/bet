import uuid
from typing import Union, Dict, Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from tortoise.expressions import Q

from accounts.logger import get_logger
from accounts.models import User
from accounts.schemas import LoginSuccess, UserLogin, UserRegister, user_pydantic_model
from accounts.utils import (
    generate_hashed_password,
    generate_jwt_token,
    generate_verify_token,
    send_verification_message_background,
    verify_token,
)

auth_router = APIRouter(prefix="", tags=["auth"])
logger = get_logger("Auth")


@auth_router.post("/register")
async def register(
    background_tasks: BackgroundTasks, register_body: UserRegister
) -> Union[User, HTTPException]:
    if await User.get_or_none(email=register_body.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже зарегистрирован",
        )
    try:
        hashed_password, salt = generate_hashed_password(register_body.password)
        user = await User.create(
            id=uuid.uuid4(),
            email=register_body.email,
            first_name=register_body.first_name,
            password=hashed_password,
            username=register_body.username,
            salt=salt,
        )
        token = generate_verify_token(user.email)
        await send_verification_message_background(
            background_tasks, register_body.email, token
        )
        return await user_pydantic_model.from_tortoise_orm(user)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидное тело запроса"
        )


@auth_router.post(
    "/login",
    response_model=LoginSuccess,
)
async def login(login_body: UserLogin) -> Union[Dict[str, str], HTTPException]:
    try:
        user = await User.get_or_none(Q(email=login_body.email))
        if not user:
            logger.error("Пользователь с email %s не найден", login_body.email)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с email {login_body.email} не найден",
            )
        hashed_password, salt = generate_hashed_password(
            login_body.password, salt=user.salt
        )
        if not hashed_password == user.password:
            logger.error("Неверный пароль")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль"
            )
        return generate_jwt_token(user.email)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидное тело запроса"
        )


templates = Jinja2Templates(directory="templates")


@auth_router.get("/verify", response_class=HTMLResponse)
async def verify(request: Request, token: str) -> Any:
    """
    Верификация пользователя
    """
    user = await verify_token(token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse(
            "verify-email.html", {"request": request, "username": user.username}
        )