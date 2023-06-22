from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Poster, User, Response
from .forms import PosterForm, ResponseForm
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from .filters import PosterFilter
import os
from dotenv import load_dotenv
load_dotenv()


class PosterList(ListView):
    model = Poster
    ordering = '-created'
    template_name = 'poster_list.html'
    context_object_name = 'poster_list'
    paginate_by = 5


class PosterDetail(DetailView):
    model = Poster
    template_name = 'poster_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poster_author'] = self.get_object().user == self.request.user
        return context


class PosterCreate(LoginRequiredMixin, CreateView):
    model = Poster
    template_name = 'poster_edit.html'
    form_class = PosterForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        return result


class PosterEdit(LoginRequiredMixin, UpdateView):
    model = Poster
    form_class = PosterForm

    def get_template_names(self):
        poster = self.get_object()
        if poster.user == self.request.user:
            self.template_name = 'poster_edit.html'
        else:
            self.template_name = '403.html'
        return self.template_name


class PosterDelete(LoginRequiredMixin, DeleteView):
    model = Poster
    success_url = reverse_lazy('poster_list')

    def get_template_names(self):
        poster = self.get_object()
        if poster.user == self.request.user:
            self.template_name = 'poster_delete.html'
        else:
            self.template_name = '403.html'
        return self.template_name


class PosterSearch(ListView):
    model = Poster
    ordering = '-created'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PosterFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'response_list.html'
    context_object_name = 'response_list'
    ordering = '-created'

    def get_queryset(self):
        queryset = Response.objects.filter(poster__user=self.request.user)
        return queryset


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response

    def get_template_names(self):
        response = self.get_object()
        if self.request.user == response.poster.user:
            self.template_name = 'response_detail.html'
            return self.template_name
        else:
            raise PermissionDenied


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'response_create.html'
    form_class = ResponseForm
    success_url = '/success/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.poster = Poster.objects.get(id=self.kwargs['pk'])
        self.object.save()
        result = super().form_valid(form)
        response_url = self.request.build_absolute_uri(reverse('response_detail', args=[self.object.pk]))
        send_mail(
            subject=f'Response for "{self.object.poster.title}"',
            message=f'Response content: "{self.object.text}".\nYou can view the response here: {response_url}',
            from_email=os.getenv('EMAIL_HOST_USER') + '@yandex.ru',
            recipient_list=[self.object.poster.user.email]
        )
        return result


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'success.html'


@login_required()
def approve_response(request, pk):
    response = Response.objects.get(pk=pk)
    response.status = 'A'
    response.save()
    poster_url = request.build_absolute_uri(reverse('poster_detail', args=[response.poster.pk]))
    send_mail(
        subject=f'Bulletin Board: your response is approved',
        message=f'Your response for "{response.poster.title}" is approved. You can view the poster here: {poster_url}',
        from_email=os.getenv('EMAIL_HOST_USER') + '@yandex.ru',
        recipient_list=[response.user.email]
    )
    return HttpResponseRedirect(reverse('response_list'))


@login_required()
def reject_response(request, pk):
    response = Response.objects.get(pk=pk)
    response.status = 'R'
    response.save()
    return HttpResponseRedirect(reverse('response_list'))
