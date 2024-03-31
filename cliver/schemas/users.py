from typing import Optional
from uuid import UUID

from pydantic import BaseModel as Schema, ConfigDict
from pydantic.networks import EmailStr

from cliver.models.user import UserRole, UserAccountType


class UserSchema(Schema):

    id: int
    uid: UUID
    username: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: UserRole
    account_type: UserAccountType

    model_config = ConfigDict(
        from_attributes=True
    )
