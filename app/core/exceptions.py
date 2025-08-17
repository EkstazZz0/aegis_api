from fastapi import HTTPException, status

user_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with the provided data already exists"
    )

auth_ivalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password"
)

auth_expired_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired"
)

auth_token_invalid = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token invalid"
)

auth_token_inactive = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token inactive"
)
