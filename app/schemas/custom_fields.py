from pydantic.functional_validators import AfterValidator
from typing import Annotated
import re

from app.core.exceptions import invalid_phone_number, invalid_username


def validate_phone_number(v: str):
        phone_regex = r"^\+7\d{10}$"

        if not re.match(phone_regex, v):
            raise invalid_phone_number

        return v


def validate_username(v: str):
      if not v.isascii() or " " in v:
            raise invalid_username
      
      return v


def validate_password(v: str):
      if len(v.replace(' ', '')) < 8:
            raise ValueError("Password too short, use at least 8 symbols")
      
      if len(v) > 256:
            raise ValueError("Password too long, use at max 256 symbols")
      
      if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one capital letter")
      
      if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
      
      if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
      
      return v
      

PhoneNumber = Annotated[str, AfterValidator(validate_phone_number)]
Password = Annotated[str, AfterValidator(validate_password)]
