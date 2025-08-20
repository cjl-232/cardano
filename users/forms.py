from django.forms import ModelForm

from .models import Gender, Profile
from organisation.models import Grade, Profession, Unit


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
