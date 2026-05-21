from datetime import UTC, datetime, timedelta

from jose import ExpiredSignatureError, JWTError, jwt

from realworld.config import get_settings
from realworld.errors import ExpiredToken, InvalidToken


def encode_token(user_id: int) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except ExpiredSignatureError as exc:
        raise ExpiredToken() from exc
    except JWTError as exc:
        raise InvalidToken() from exc
