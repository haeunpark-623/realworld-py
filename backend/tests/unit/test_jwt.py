import pytest

from realworld.config import get_settings
from realworld.errors import ExpiredToken, InvalidToken
from realworld.utils.jwt import decode_token, encode_token


def test_encode_decode_round_trip() -> None:
    token = encode_token(user_id=1)
    payload = decode_token(token)
    assert payload["sub"] == "1"
    assert "exp" in payload


def test_decode_expired_raises_expired_token(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    settings = get_settings()
    monkeypatch.setattr(settings, "JWT_EXPIRE_MINUTES", -1)

    token = encode_token(user_id=1)
    with pytest.raises(ExpiredToken):
        decode_token(token)

    get_settings.cache_clear()


def test_decode_tampered_raises_invalid_token() -> None:
    token = encode_token(user_id=1)
    tampered = token[:-4] + ("AAAA" if token[-4:] != "AAAA" else "BBBB")
    with pytest.raises(InvalidToken):
        decode_token(tampered)
