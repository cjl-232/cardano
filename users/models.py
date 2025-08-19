from django.contrib.auth.models import AbstractUser
from django.db import models

from organisation.models import Grade, Profession, Unit


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        unique=True,
    )
    gender: models.ForeignKey['Gender'] = models.ForeignKey(
        to='Gender',
        on_delete=models.PROTECT,
        related_name='+',
    )
    grade: models.ForeignKey[Grade] = models.ForeignKey(
        to=Grade,
        on_delete=models.PROTECT,
        related_name='users',
    )
    profession: models.ForeignKey[Profession] = models.ForeignKey(
        to=Profession,
        on_delete=models.PROTECT,
        related_name='users',
    )
    unit: models.ForeignKey[Unit] = models.ForeignKey(
        to=Unit,
        on_delete=models.PROTECT,
        related_name='users',
    )
    years_as_analyst = models.PositiveSmallIntegerField()
    years_at_current_grade = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'users_users'


class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'users_genders'
