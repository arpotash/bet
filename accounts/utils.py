import random
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Dict, Optional, Tuple, Union

import bcrypt
import jwt
from fastapi import BackgroundTasks, HTTPException, status

from accounts.config import email_config, settings
from accounts.models import User
from accounts.routers import logger
from fastapi_mail import FastMail, MessageSchema
from tortoise.exceptions import DoesNotExist


async def send_verification_message_background(
    background_tasks: BackgroundTasks, email: str, token: str
) -> None:
    """
    Отправка верификационного письма на почту
    """
    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
            </head>
            <body>
                <div style = "display: flex; align-items: center; justify-content:
                center; flex-direction: column">

                    <h3>Account Verification </h3>
                    <br>
                    <p>Thanks for choosing FitnessApp, please click on the button below to verify your account </p>
                    <a style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; 
                    font-size: 1rem; text-decoration: none; #0275d8; color: white;" 
                    href="http://localhost:8000/verify/?token={token}">
                    Verify your email
                    </a>
                    <p>Please kindly ignore this email if you did not register for 
                    FitnessApp and nothing will happend. Thanks</p>
                </div>
            </body>
        </html>
    """
    message = MessageSchema(
        subject="FitnessApp Verification Email",
        recipients=[email],
        html=template,
        subtype="html",
    )
    fm = FastMail(email_config)
    background_tasks.add_task(fm.send_message, message)


def generate_jwt_token(username: str) -> Dict[str, str]:
    """
    jwt token generation (access и refresh)
    """
    access_token = jwt.encode(
        {
            "username": username,
            "count": random.random(),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        key=settings.secret,
        algorithm=settings.algorithm,
    )
    refresh_token = jwt.encode(
        {
            "username": username,
            "count": random.random(),
            "exp": datetime.now(timezone.utc) + timedelta(days=14),
        },
        key=settings.secret,
        algorithm=settings.algorithm,
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def generate_verify_token(username: str) -> str:
    """
    Verification token generation
    """
    token = jwt.encode(
        {
            "user": username,
            "count": random.random(),
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
        },
        key=settings.secret,
        algorithm=settings.algorithm,
    )
    return token


def generate_hashed_password(
    password: str, salt: Optional[str] = ""
) -> Tuple[str, str]:
    """
    Token hashing
    """
    if not salt:
        unique_salt = bcrypt.gensalt(8).decode()
    else:
        unique_salt = salt
    password = ".".join([password, unique_salt, settings.password_salt])
    hashed_password = sha256(password.encode()).hexdigest()
    return hashed_password, unique_salt


async def verify_token(
    token: str,
) -> Union[User, DoesNotExist]:
    """
    Token decryption
    """
    try:
        payload = jwt.decode(token, settings.secret, algorithms=settings.algorithm)
        user = await User.get(username=payload.get("user"))
        return user
    except DoesNotExist as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
