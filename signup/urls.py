from django.urls import path, re_path
from django.conf.urls import url, handler404

from . import views

app_name = 'signup'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register, name='register'),
    path('<link>', views.activate, name='activate'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]