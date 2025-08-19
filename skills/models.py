from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'skills_skills'


class SkillEntry(models.Model):
    class Proficiency(models.IntegerChoices):
        NONE = 0, _('No knowledge or experience')
        AWARENESS = 1, _('Knowledge but no experience')
        LIMITED_EXPERIENCE = 2, _('Limited experience')
        MODERATE_EXPERIENCE = 3, _('Moderate experience')
        GOOD_EXPERIENCE = 4, _('Good experience')

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='skill_entries',
    )
    skill = models.ForeignKey(
        to=Skill,
        on_delete=models.PROTECT,
        related_name='entries',
    )
    proficiency = models.SmallIntegerField(choices=Proficiency.choices)
    used_in_last_six_months = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skills_skill_entries'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'skill'],
                name='skills_skill_entries_AK01',
            )
        ]

# Create your models here.

# Nested categories? Seems reasonable... then in the UI, nested dropdowns