from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('modules', views.modules, name='modules'),
    path('sql_classic', views.sql_classic, name='sql_classic'),
]

