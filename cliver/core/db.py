import uuid

from django.db import models


class BaseAbstractModel(models.Model):
    
    """Default model with basic fields"""

    class Meta:
        abstract = True

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    uid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
