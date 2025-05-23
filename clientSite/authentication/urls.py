from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signin', views.login, name='signin'),
    path('signup', views.register, name='signup'),
    ]
