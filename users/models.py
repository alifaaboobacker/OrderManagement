# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("staff", "Staff"),
        ("partner", "Partner"),
        ("admin", "Admin")
    ]

    contact_number = models.IntegerField(null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
