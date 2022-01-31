from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class contact(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    firstName = models.CharField(max_length=25, null=True)
    lastName = models.CharField(max_length=25, null=True)
    number = models.CharField(max_length=11, null=True)
    note = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.firstName, self.lastName)

