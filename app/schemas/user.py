from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


def normalize_phone_number(value):
    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("Phone number must be a string or integer")

    phone_number = str(value).strip()

    if not phone_number:
        raise ValueError("Phone number cannot be empty")

    return phone_number


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str | None = None
    device_token: str | None = None

    normalize_phone = field_validator(
        "phone_number",
        mode="before"
    )(normalize_phone_number)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str | None = None
    device_token: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str | None = None
    device_token: str | None = None

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    device_token: str | None = None

    normalize_phone = field_validator(
        "phone_number",
        mode="before"
    )(normalize_phone_number)
