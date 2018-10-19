from django.db import models
from django.contrib.auth.models import User

class Notfication(models.Model):
    new_sub =  models.BooleanField(default=False)
    re_subbed =  models.BooleanField(default=False)
    like =  models.BooleanField(default=False)
    comment =  models.BooleanField(default=False)
    points_add =  models.BooleanField(default=False)
    points_spent =  models.BooleanField(default=False)
    transactions =  models.BooleanField(default=False)
    tip =  models.BooleanField(default=False)
    user = models.OneToOneField(User, default='')
