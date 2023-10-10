from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from articles.models import Style


class UserManager(BaseUserManager):
    def create_user(self, password, **fields):
        user = self.model(**fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **fields):
        fields.setdefault("is_admin", True)
        fields.setdefault("is_superuser", True)
        user = self.create_user(**fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        "username",
        max_length=64,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        "email",
        max_length=128,
        unique=True,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="followees", blank=True
    )
    nickname = models.CharField(
        "nickname", max_length=32, unique=True, blank=True, null=True
    )
    image = models.ImageField(upload_to="profile_pics", blank=True)
    styles = models.ManyToManyField(Style, related_name="users", blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.nickname

    @property
    def is_staff(self):
        return self.is_admin
