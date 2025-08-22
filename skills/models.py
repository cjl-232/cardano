import functools

from dataclasses import dataclass
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    id: models.BigAutoField
    skills: models.QuerySet['Skill']
    children: models.QuerySet['Category']
    name = models.CharField(max_length=255)
    parent: models.ForeignKey['Category | None'] = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True,
    )

    @dataclass
    class _SkillTreeNode:
        name: str
        skills: models.QuerySet['Skill'] | list['Skill']
        has_skills: bool
        subnodes: list['Category._SkillTreeNode']
        entry_forms: dict[str, forms.Form]

        def add_forms(self, mapping: dict[int, forms.Form]):
            for skill in self.skills:
                self.entry_forms[skill.name] = mapping[skill.id]
            for subnode in self.subnodes:
                subnode.add_forms(mapping)

    @staticmethod
    @functools.cache
    def _make_tree_node(category: 'Category') -> _SkillTreeNode:
        node = Category._SkillTreeNode(
            name=category.name,
            skills=category.skills.order_by('name'),
            has_skills=category.skills.exists(),
            subnodes=[],
            entry_forms={},
        )
        for subcategory in category.children.order_by('name'):
            subnode = Category._make_tree_node(subcategory)
            if subnode.has_skills:
                node.has_skills = True
                node.subnodes.append(subnode)
        return node

    @classmethod
    def make_tree(cls, mapping: dict[int, forms.Form]) -> _SkillTreeNode:
        top_level = cls.objects.filter(parent=None).order_by('name')
        top_nodes = [cls._make_tree_node(category) for category in top_level]
        root = Category._SkillTreeNode(
            name='Root',
            skills=[],
            has_skills=any([node.has_skills for node in top_nodes]),
            subnodes=top_nodes,
            entry_forms={},
        )
        root.add_forms(mapping)
        return root

    def clean(self):
        ancestor = self.parent
        while ancestor is not None:
            if ancestor.id == self.id:
                raise ValidationError('Loop detected in parent chain.')
            ancestor = ancestor.parent

    def save(self, *args: Any, **kwargs: Any):
        self._make_tree_node.cache_clear()
        self.full_clean()
        return super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any):
        self._make_tree_node.cache_clear()
        return super().delete(*args, **kwargs)

    def __str__(self):
        if self.parent is not None:
            return f'{str(self.parent)} -> {self.name}'
        else:
            return self.name

    class Meta:
        db_table = 'skills_categories'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'parent'],
                name='skills_categories_AK01',
            ),
        ]


class Skill(models.Model):
    id: models.BigAutoField
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='skills',
    )

    def __str__(self):
        return f'{str(self.category)}: {self.name}'

    class Meta:
        db_table = 'skills_skills'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='skills_skills_AK01',
            ),
        ]


class SkillEntry(models.Model):
    class Proficiency(models.IntegerChoices):
        NONE = 0, _('No knowledge or experience')
        AWARENESS = 1, _('Knowledge but no experience')
        LIMITED_EXPERIENCE = 2, _('Limited experience')
        MODERATE_EXPERIENCE = 3, _('Moderate experience')
        GOOD_EXPERIENCE = 4, _('Good experience')

    id: models.BigAutoField
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
    proficiency = models.SmallIntegerField(
        choices=Proficiency.choices,
    )
    used_in_last_six_months = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Entry #{self.id}'

    class Meta:
        db_table = 'skills_skill_entries'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'skill'],
                name='skills_skill_entries_AK01',
            ),
        ]

# Create your models here.

# Nested categories? Seems reasonable... then in the UI, nested dropdowns