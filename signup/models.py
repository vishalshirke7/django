from django.db import models
# Create your models here.
from mongoengine import *
from myproj.settings import DBNAME

connect(DBNAME)


class User(Document):
    fname = StringField(max_length=20, required=True)
    lname = StringField(max_length=20, required=True)
    email = EmailField(max_length=200, required=True)
    active = BooleanField()
    verf_link = StringField(max_length=200)
    password =  StringField(max_length=200)
