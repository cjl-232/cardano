from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from organisation.models import Grade, Profession, Unit


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    profile: 'Profile'
    email = models.EmailField(unique=True)
    username = None

    class Meta:
        db_table = 'users_users'


class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users_genders'


class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
    )
    gender = models.ForeignKey(
        to=Gender,
        on_delete=models.PROTECT,
        related_name='+',
    )
    grade: models.ForeignKey[Grade] = models.ForeignKey(
        to=Grade,
        on_delete=models.PROTECT,
        related_name='+',
    )
    profession: models.ForeignKey[Profession] = models.ForeignKey(
        to=Profession,
        on_delete=models.PROTECT,
        related_name='+',
    )
    unit: models.ForeignKey[Unit] = models.ForeignKey(
        to=Unit,
        on_delete=models.PROTECT,
        related_name='+',
    )
    years_as_analyst = models.PositiveSmallIntegerField()
    years_at_current_grade = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Details for {self.user.email}'

    class Meta:
        db_table = 'users_profiles'
