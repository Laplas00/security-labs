from django.urls import path
from . import views, toolkit_for_labs


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('modules', views.modules, name='modules'),
    path('sql_classic', views.sql_classic, name='sql_classic'),
    path('start_lab_for_user', toolkit_for_labs.start_lab_for, name='start_lab_for_user'),
]


from django.urls import path
from . import toolkit_for_labs as labs

urlpatterns = [
    path('lab/sql_injection_classic/start', labs.start_lab, name="start_lab"),
    path('lab/sql_injection_classic/stop', labs.stop_lab, name="stop_lab"),
]

