# pyright: reportMissingTypeArgument=false

from django.contrib import admin

from .models import Gender, User


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass