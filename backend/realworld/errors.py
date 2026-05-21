class RealWorldError(Exception):
    status_code: int = 500
    message: str = "내부 오류가 발생했습니다"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.message)
        if message is not None:
            self.message = message


class DuplicateEmail(RealWorldError):
    status_code = 422
    message = "이미 사용 중인 이메일입니다"


class DuplicateUsername(RealWorldError):
    status_code = 422
    message = "이미 사용 중인 사용자명입니다"


class InvalidCredentials(RealWorldError):
    status_code = 401
    message = "이메일 또는 비밀번호가 올바르지 않습니다"


class InvalidToken(RealWorldError):
    status_code = 401
    message = "인증 토큰이 유효하지 않습니다"


class ExpiredToken(RealWorldError):
    status_code = 401
    message = "인증 토큰이 만료되었습니다"


class Forbidden(RealWorldError):
    status_code = 403
    message = "권한이 없습니다"


class NotFound(RealWorldError):
    status_code = 404
    message = "리소스를 찾을 수 없습니다"
