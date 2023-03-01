from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False,
                    is_active=True, phone_number=None, **extra_fields):
        'Creates a User with the given username, email and password'

        user = self.model(is_active=is_active,
                          is_staff=is_staff, **extra_fields)
        if email:
            email = UserManager.normalize_email(email)
            user.email = email

        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True,
                                is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField('User Phone', max_length=100, unique=True, blank=True, null=True)
    nickname = models.CharField('nickname', max_length=200, blank=False, null=False, )
    firstname = models.CharField(max_length=200, blank=True, null=True, )
    lastname = models.CharField(max_length=200, blank=True, null=True, )

    is_staff = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, null=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.firstname} {self.lastname} {self.phone}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]
        get_latest_by = "date_joined"
