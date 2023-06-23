from random import randint
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from .forms import BaseRegisterForm, LoginForm, CodeLoginForm
from .models import CheckCode
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from django.conf import settings


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/account/login'


def login_view(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                code = CheckCode.objects.create(code=randint(100000, 999999), user=user)
                send_mail(
                    subject='Bulletin Board: your verification code',
                    message=f'Code: {code.code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email]
                )
                return redirect('/account/code')
            else:
                message = 'Invalid login or password'
    return render(request, 'login.html', context={'form': form, 'message': message})


def code_view(request):
    form = CodeLoginForm()
    message = ''
    if request.method == 'POST':
        form = CodeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                message = 'User does not exist'
                return render(request, 'code.html', context={'form': form, 'message': message})
            if CheckCode.objects.filter(code=code, user__username=username).exists():
                login(request, user)
                return redirect('/')
            else:
                message = 'Invalid code'
    return render(request, 'code.html', context={'form': form, 'message': message})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
