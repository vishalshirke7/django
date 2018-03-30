from django.db import models

class User(models.Model):
    user_fname = models.CharField(max_length=200)
    user_lname = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_isactive = models.BooleanField()    
