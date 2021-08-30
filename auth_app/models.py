from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    username = None
    groups=None
    user_permissions=None
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    class Meta:
        db_table = "auth_user"
        unique_together = ('email', 'name',)
