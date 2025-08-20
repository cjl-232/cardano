# pyright: reportMissingTypeArgument=false

from django.contrib import admin

from .models import Grade, Profession, Unit


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
