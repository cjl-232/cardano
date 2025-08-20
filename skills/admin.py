# pyright: reportMissingTypeArgument=false

from django.contrib import admin

from .models import Category, Skill, SkillEntry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', '__str__']


@admin.register(SkillEntry)
class SkillEntryAdmin(admin.ModelAdmin):
    pass
