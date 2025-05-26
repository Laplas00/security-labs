from django.urls import path
from . import views, toolkit_for_labs
from . import toolkit_for_labs as labs 

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('modules', views.modules, name='modules'),
    path('sql_classic', views.sql_classic, name='sql_classic'),
    path('start_lab', labs.start_lab, name="start_lab"),
    path('stop_lab', labs.stop_lab, name="stop_lab"),
]

