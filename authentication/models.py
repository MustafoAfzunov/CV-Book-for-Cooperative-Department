from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_pending = models.BooleanField(default=True)  # True for pending approval
    approved_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_users')

    def __str__(self):
        return self.username