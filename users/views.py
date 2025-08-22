from typing import cast

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_not_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm
from .models import User


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


def view_profile(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    if not hasattr(user, 'profile'):
        return redirect('users:edit_profile')
    profile = user.profile
    return render(request, 'users/view_profile.html', {'profile': profile})


@login_not_required
def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', 'skills:overview'))
    match request.method:
        case 'GET':
            form = LoginForm()
        case 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                try:
                    user = get_user_model().objects.get(email=email)
                    if not user.check_password(password):
                        raise ValueError('Incorrect password.')
                    login(request, user)
                    return redirect(request.GET.get('next', 'skills:overview'))
                except (ObjectDoesNotExist, ValueError):
                    form.add_error(None, 'Invalid email or password.')
        case _:
            return HttpResponseNotAllowed(['GET', 'POST'])
    return render(request, 'users/login.html', {'form': form})


@require_POST
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('users:login')
