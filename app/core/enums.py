from enum import Enum


class AppEnv(str, Enum):
    production = "production"
    test = "test"


class UserRole(str, Enum):
    customer = "customer"
    resolver = "resolver"
    admin = "admin"


class RequestStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
