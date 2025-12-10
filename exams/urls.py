from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/exams/', views.api_exams, name='api_exams'),
    path('api/departments/', views.api_departments, name='api_departments'),
]


