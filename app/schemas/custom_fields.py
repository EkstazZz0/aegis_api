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
      


      

PhoneNumber = Annotated[str, AfterValidator(validate_phone_number)]
