from django.urls import path

from .views import edit_profile, view_profile, skills_list

app_name = 'users'
urlpatterns = [
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('skills/', skills_list, name='skills_list'),
]
