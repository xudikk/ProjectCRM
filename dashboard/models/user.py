from django.db import models
from django.utils import timezone



class Otp(models.Model):
    key = models.CharField(max_length=512)
    mobile = models.CharField()
    is_expired = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
    extra = models.JSONField(default={})
    is_verified = models.BooleanField(default=False)
    step = models.CharField()
    by = models.CharField(choices=[
        ("by regis", "By Register"),
        ("by login", "By Login"),
    ])

    created = models.DateTimeField(auto_now=False, default=timezone.now, auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.key}-{self.mobile}"




