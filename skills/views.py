from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import SkillEntryFormset
from .models import Category, Skill, SkillEntry


@login_required
def overview(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        initial: list[dict[str, Any]] = []
        entries = SkillEntry.objects.filter(user=request.user)
        entries_lookup = {entry.skill.id: entry for entry in entries}
        for skill in Skill.objects.all():
            entry = entries_lookup.get(skill.id)
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
        mapping = {form.initial['skill_id']: form for form in formset}
    elif request.method == 'POST':
        formset = SkillEntryFormset(data=request.POST)
        for form in formset:
            if not form.has_changed() or not form.is_valid():
                continue
            proficiency = form.cleaned_data['proficiency']
            used_recently = form.cleaned_data['used_in_last_six_months']
            entry, created = SkillEntry.objects.get_or_create(
                user=request.user,
                skill=form.cleaned_data['skill'],
                defaults={
                    'proficiency': proficiency,
                    'used_in_last_six_months': used_recently,
                },
            )
            if not created:
                if entry.proficiency == proficiency:
                    if entry.used_in_last_six_months == used_recently:
                        continue
                entry.proficiency = proficiency
                entry.used_in_last_six_months = used_recently
                entry.save()
        mapping = {form.cleaned_data['skill_id']: form for form in formset}
        return redirect('skills:overview')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    tree = Category.make_tree(mapping)
    context = {
        'formset': formset,
        'tree': tree,
    }
    return render(request, 'skills/overview.html', context)
