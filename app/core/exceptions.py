from fastapi import HTTPException, status

user_already_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with the provided data already exists"
    )

auth_ivalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password"
)
