from django.urls import path

from .views import matrix, overview

app_name = 'skills'
urlpatterns = [
    path('', overview, name='overview'),
    path('matrix/', matrix, name='matrix'),
]
