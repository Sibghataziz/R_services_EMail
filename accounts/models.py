from django.db import models
from django.contrib.auth.models import User
# Create your models here.

nature = [("Doctor","Doctor"),("Patient","Patient")]
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numberOfMails = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username
