from django.urls import path, re_path
from django.conf.urls import url

from . import views

app_name = 'signup'
urlpatterns=[
	path('',views.index,name='index'),
	path('signup/',views.register,name='register'),
	path('verify/',views.verify,name='verify'),
    path('<slug:uidb64>/<slug:token>',views.activate, name='activate'),
]
