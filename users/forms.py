from django.forms import ModelForm, RadioSelect

from .models import Gender, Profile
from organisation.models import Grade, Profession, Unit
from skills.models import Skill, SkillEntry


class ProfileForm(ModelForm):
    gender: Gender
    grade: Grade
    profession: Profession
    unit: Unit
    years_as_analyst: int
    years_at_current_grade: int

    class Meta:
        model = Profile
        fields = [
            'gender',
            'grade',
            'profession',
            'unit',
            'years_as_analyst',
            'years_at_current_grade',
        ]


class SkillEntryForm(ModelForm):
    skill: Skill

    class Meta:
        model = SkillEntry
        fields = [
            'proficiency',
            'used_in_last_six_months',
        ]
        widgets = {
            'proficiency': RadioSelect(),
        }
