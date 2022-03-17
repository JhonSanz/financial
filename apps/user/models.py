
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    identification = models.CharField(
        max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Extended User"
        ordering = ['-id']

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()
