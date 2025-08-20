from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import User
from skills.models import Category


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


@login_required
def skills(request: HttpRequest) -> HttpResponse:
    top_categories = Category.objects.filter(parent=None)
    return render(request, 'users/skills.html', {'top_categories': top_categories})