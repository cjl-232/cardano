from django.urls import path

from .views import overview

app_name = 'skills'
urlpatterns = [
    path('', overview, name='overview'),
]
