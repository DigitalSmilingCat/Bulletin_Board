from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import BaseRegisterView, login_view, code_view, ProfileView, edit_profile_view
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('login/',
         login_view,
         name='login'),
    path('code/',
         code_view,
         name='code'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),
    path('profile/',
         ProfileView.as_view(),
         name='profile'),
    path('change_password/', PasswordChangeView.as_view(
         template_name='password_change_form.html',
         success_url='/account/profile'),
         name='change-password'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
]