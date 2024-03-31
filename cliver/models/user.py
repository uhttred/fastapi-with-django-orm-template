import unicodedata

from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint, CheckConstraint
from django.core.exceptions import ObjectDoesNotExist

from argon2.exceptions import VerifyMismatchError

from cliver.core.db import BaseAbstractModel
from cliver.core.security import (
    hash_password,
    verify_password
)


class UserRole(models.TextChoices):
    SUPERMANAGER = 'supermanager'
    OPERATOR = 'operator'


class UserAccountType(models.TextChoices):
    MANAGER = 'manager'
    CUSTOMER = 'customer'


class UserManager(models.Manager['User']):

    async def get_by_username(self, username: str) -> 'User | None':
        try:
            user = await self.aget(username__iexact=username)
        except ObjectDoesNotExist:
            return None
        return user
    
    async def get_by_email(self, email: str) -> 'User | None':
        try:
            user = await self.aget(email=email.lower())
        except ObjectDoesNotExist:
            return None
        return user


class User(BaseAbstractModel):

    class Meta:  # type: ignore
        db_table = 'user'
        app_label = 'cliver'
        constraints = (
            UniqueConstraint(
                Lower('username'),
                name='unique_user_username'
            ),
            UniqueConstraint(
                Lower('email'),
                name='unique_user_email'
            ),
            CheckConstraint(
                check=models.Q(account_type__in=UserAccountType.values),
                name='check_account_type_valid_choices'
            ),
            CheckConstraint(
                check=models.Q(role__in=UserRole.values),
                name='check_user_role_valid_choices'
            )
        )

    AccountType = UserAccountType
    Role = UserRole

    profile: 'UserProfile'
    query = UserManager()

    name = models.CharField(max_length=44, null=True, default=None)
    username = models.CharField(max_length=20, unique=True, null=False)
    email = models.CharField(max_length=250, null=True, default=None)
    password = models.CharField(max_length=228, null=True, default=None)
    is_active = models.BooleanField(default=True)

    role = models.CharField(
        max_length=12,
        choices=Role.choices
    )
    account_type = models.CharField(
        max_length=8,
        choices=AccountType.choices,
        default=AccountType.CUSTOMER
    )

    @classmethod
    def normalize_username(cls, username: str | None):
        if isinstance(username, str):
            return unicodedata.normalize('NFKC', username)
        return username
    
    def clean(self) -> None:
        super().clean()
        self.username = self.normalize_username(self.username)
        self.email = self.email.lower() if self.email else None
    
    def set_password(self, password: str) -> None:
        """Hash a plain password and set to the model"""
        self.password = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Checks user password"""
        if self.password:
            try:
                return verify_password(hash=self.password, password=password)
            except VerifyMismatchError: ...
        return False
    

# for typing support
from .user_profile import UserProfile
