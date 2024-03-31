from pydantic import BaseModel as Schema
from pydantic.networks import EmailStr


class AuthenticationSchema(Schema):

    email: EmailStr
    password: str
    