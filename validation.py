import re
from typing import Type, Optional

import pydantic

from app import bcrypt
from errors import HttpError

password_regex = re.compile(
    "^(?=.*[a-z_])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,200}$"
)

email_regex = re.compile(
    "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


class CreateUserSchema(pydantic.BaseModel):
    name: str
    email: str
    password: str

    @pydantic.validator("name")
    def check_name(cls, value: str):
        if len(value) > 100:
            raise ValueError("name mast be less 32 chars")

        return value

    @pydantic.validator("email")
    def check_email(cls, value: str):
        if not re.search(email_regex, value):
            raise ValueError("email is wrong")

        return value

    @pydantic.validator("password")
    def check_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError("password to easy")

        value.encode()
        value = bcrypt.generate_password_hash(value, rounds=None)
        value = value.decode()

        return value


class PatchUserSchema(pydantic.BaseModel):
    name: Optional[str]
    email: str
    password: Optional[str]

    @pydantic.validator("password")
    def check_name(cls, value: str):
        if len(value) > 32:
            raise ValueError("name mast be less 32 chars")

        return value

    @pydantic.validator("email")
    def check_email(cls, value: str):
        if not re.search(email_regex, value):
            raise ValueError("email is wrong")

        return value

    @pydantic.validator("password")
    def check_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError("password to easy")

        value = value.encode()
        value = bcrypt.generate_password_hash(value)
        value = value.decode()

        return value


class CreateAdvSchema(pydantic.BaseModel):
    title: str
    description: str

    @pydantic.validator("title")
    def check_title(cls, value: str):
        if len(value) > 200:
            raise ValueError("The title length mast be less 200 chars")

        return value

    @pydantic.validator("description")
    def check_description(cls, value: str):
        if len(value) > 2000:
            raise ValueError("The advertisement length mast be less 2000 chars")

        return value

class PatchAdvSchema(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]

    @pydantic.validator("title")
    def check_title(cls, value: str):
        if len(value) > 200:
            raise ValueError("The title length mast be less 200 chars")

        return value

    @pydantic.validator("description")
    def check_description(cls, value: str):
        if len(value) > 2000:
            raise ValueError("The advertisement length mast be less 2000 chars")

        return value


def validate(data_to_validate: dict,
             validation_class: Type[CreateUserSchema] | Type[PatchUserSchema] | Type[CreateAdvSchema]):
    try:
        return validation_class(**data_to_validate).dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())