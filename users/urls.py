from django.urls import path

from .views import edit_profile, login_view, logout_view, view_profile

app_name = 'users'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
