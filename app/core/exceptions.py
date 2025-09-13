from fastapi import HTTPException, status

user_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with the provided data already exists",
)

user_blocked = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User blocked"
)

auth_ivalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
)

auth_expired_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
)

auth_token_invalid = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid"
)

auth_token_inactive = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inactive"
)

medical_organisation_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Medical organisation not found"
)

medical_organisation_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A medical organisation with the provided data already exists",
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

invalid_phone_number = ValueError("Invalid phone number")

invalid_username = ValueError("Invalid username")

invlaid_change_password = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Provided password invalid"
)

service_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
)

request_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
)

request_forbidden = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Request not available"
)

comment_forbidden = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Comment not available"
)

comment_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
)

forbidden = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

session_not_found = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not found"
)
