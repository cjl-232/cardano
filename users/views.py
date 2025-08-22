from dataclasses import dataclass
from functools import cache
from typing import Any, cast

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import ProfileForm, SkillEntryForm
from .models import User
from skills.models import Category, Skill, SkillEntry


_SkillEntryFormSet = modelformset_factory(
    model=SkillEntry,
    fields=[
        'skill',
        'proficiency',
        'used_in_last_six_months',
    ],
    can_delete=True,
)


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    instance = getattr(user, 'profile', None)
    match request.method:
        case 'GET':
            form = ProfileForm(instance=instance)
        case 'POST':
            form = ProfileForm(data=request.POST, instance=instance)
            if form.is_valid():
                if instance is None:
                    instance = form.save(commit=False)
                    instance.user = request.user
                instance.save()
                return redirect('users:view_profile')
        case _:
            return HttpResponseNotAllowed(['GET', 'POST'])
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def view_profile(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    if not hasattr(user, 'profile'):
        return redirect('users:edit_profile')
    profile = user.profile
    return render(request, 'users/view_profile.html', {'profile': profile})


class _SkillsTreeNode:
    def __init__(
            self,
            user: User,
            category: Category,
            valid_category_ids: set[int],
            valid_skill_ids: set[int],
    ):
        self.category = category
        self.subcategories: dict[str, '_SkillsTreeNode'] = {
            subcategory.name: _SkillsTreeNode(
                user,
                subcategory,
                valid_category_ids,
                valid_skill_ids,
            )
            for subcategory
            in category.children.all()
            if subcategory.id in valid_category_ids
        }
        self.skill_entry_forms: dict[str, SkillEntryForm] = {}
        for skill in category.skills.all():
            if skill.id in valid_skill_ids:
                try:
                    instance = SkillEntry.objects.get(user=user, skill=skill)
                except Exception:
                    instance = None
                self.skill_entry_forms[skill.name] = SkillEntryForm(
                    instance=instance,
                )


@login_required
def skills_list(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    formset = _SkillEntryFormSet(
        queryset=SkillEntry.objects.filter(user=user)
    )
    # Get a tree of added ones, then other ones
    skill_entries = cast(QuerySet[SkillEntry], getattr(user, 'skill_entries'))
    added_skill_ids = set([x.skill.id for x in skill_entries.all()])
    other_skill_ids: set[int] = set()
    for skill in Skill.objects.all():
        if skill.id not in added_skill_ids:
            other_skill_ids.add(skill.id)

    @cache
    def has_added(category: Category) -> bool:
        for skill in category.skills.all():
            if skill.id in added_skill_ids:
                return True
        for subcategory in category.children.all():
            if has_added(subcategory):
                return True
        return False

    @cache
    def has_other(category: Category) -> bool:
        for skill in category.skills.all():
            if skill.id not in added_skill_ids:
                return True
        for subcategory in category.children.all():
            if has_other(subcategory):
                return True
        return False


    top_categories: list[Category] = []
    added_skill_category_ids: set[int] = set()
    other_skill_category_ids: set[int] = set()
    for category in Category.objects.order_by('name').all():
        if category.parent is None:
            top_categories.append(category)
        if has_added(category):
            added_skill_category_ids.add(category.id)
        if has_other(category):
            other_skill_category_ids.add(category.id)

    added_skill_tree: dict[str, _SkillsTreeNode] = {
        category.name: _SkillsTreeNode(
            user,
            category,
            added_skill_category_ids,
            added_skill_ids,
        )
        for category
        in top_categories
        if category.id in added_skill_category_ids
    }
    other_skill_tree: dict[str, _SkillsTreeNode] = {
        category.name: _SkillsTreeNode(
            user,
            category,
            other_skill_category_ids,
            other_skill_ids,
        )
        for category
        in top_categories
        if category.id in other_skill_category_ids
    }
    context = {
        'top_categories': top_categories,
        'added_skill_ids': added_skill_ids,
        'other_skill_ids': other_skill_ids,
        'added_skill_category_ids': added_skill_category_ids,
        'other_skill_category_ids': other_skill_category_ids,
        'added_skill_tree': added_skill_tree,
        'other_skill_tree': other_skill_tree,
        'formset': formset,
    }
    print(added_skill_tree['Coding'].subcategories)
    print(other_skill_tree)
    return render(request, 'users/skills_list.html', context)
