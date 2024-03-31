from django.db import models

from cliver.core.db import BaseAbstractModel
from .user import User


class UserProfile(BaseAbstractModel):

    class Meta:  # type: ignore
        db_table = 'user_profile'
        app_label = 'cliver'

    first_name = models.CharField(max_length=34, null=True, default=None)
    last_name = models.CharField(max_length=34, null=True, default=None)
    
    owner = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
