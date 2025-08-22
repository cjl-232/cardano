from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import SkillEntryFormset
from .models import Category, Skill, SkillEntry


@login_required
def overview(request: HttpRequest) -> HttpResponse:
    # Extract current entries.
    entries_by_skill_id = {
        entry.skill.id: entry
        for entry in SkillEntry.objects.filter(user=request.user)
    }
    # Extract the skills ordered by category.
    initial: list[dict[str, Any]] = []
    for skill in Skill.objects.all():
        entry = entries_by_skill_id.get(skill.id)
        if entry is not None:
            initial.append({
                'skill_id': skill.id,
                'proficiency': entry.proficiency,
                'used_in_last_six_months': entry.used_in_last_six_months,
            })
        else:
            initial.append({
                'skill_id': skill.id,
                'proficiency': None,
                'used_in_last_six_months': False,
            })
    formset = SkillEntryFormset(initial=initial)
    for form in formset:
        print(form.initial)
    mapping = {form.initial['skill_id']: form for form in formset}
    print(mapping)
    tree = Category.make_tree(mapping)
    context = {
        'formset': formset,
        'tree': tree,
    }
    return render(request, 'skills/overview.html', context)
