from django.db import models

class User(models.Model):
    user_fname = models.CharField(max_length=80)
    user_lname = models.CharField(max_length=80)
    user_email = models.EmailField(unique=True)
    user_isactive = models.BooleanField()
    user_password = models.CharField(max_length=10)   
    user_verf_link =  models.CharField(max_length=100,default="null")
    def user_mail(self):
        return self.user_email
    
