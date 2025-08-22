from typing import Any

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Skill, SkillEntry


class SkillEntryForm(forms.Form):
    skill_id = forms.IntegerField(widget=forms.HiddenInput)
    proficiency = forms.ChoiceField(
        choices=SkillEntry.Proficiency.choices,
        widget=forms.RadioSelect,
    )
    used_in_last_six_months = forms.BooleanField(required=False)

    def clean_proficiency(self):
        data = int(self.cleaned_data['proficiency'])
        if data not in SkillEntry.Proficiency.values:
            raise ValidationError('Invalid proficiency value.')
        return data

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        try:
            skill_id = cleaned_data.get('skill_id')
            cleaned_data['skill'] = Skill.objects.get(pk=skill_id)
        except ObjectDoesNotExist:
            raise ValidationError('Skill does not exist.')
        return cleaned_data


SkillEntryFormset = forms.formset_factory(SkillEntryForm, extra=0)
