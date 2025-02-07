from fastapi import HTTPException


class AccessTokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Access token not found")


class JWKSFetchFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Failed to fetch JWKS")


class ExpiredTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Token has expired")


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid token")
