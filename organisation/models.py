from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'organisation_grades'


class Profession(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'organisation_professions'


class Unit(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'organisation_units'
