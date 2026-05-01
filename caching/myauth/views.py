from random import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, View
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.utils.translation import gettext_lazy, ngettext
from django.views.decorators.cache import cache_page

from .models import Profile
from .forms import UserEditForm, ProfileEditForm


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value {value!r} {random()}')


@permission_required('view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value {value!r}')


class UserListView(ListView):
    model = User
    template_name = 'myauth/users-list.html'
    context_object_name = 'users'


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


class UserDetailView(DetailView):
    model = User
    template_name = 'myauth/user-detail.html'
    context_object_name = 'user_info'

    def get_queryset(self):
        return super().get_queryset().select_related('profile')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'myauth/user-update-form.html'

    def get(self, request, pk):
        modified_user = get_object_or_404(User, pk=pk)
        user_form = UserEditForm(instance=modified_user)
        profile, created = Profile.objects.get_or_create(user=modified_user)
        profile_form = ProfileEditForm(instance=modified_user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'modified_user': modified_user,
        })

    def post(self, request, pk):
        modified_user = get_object_or_404(User, pk=pk)
        user_form = UserEditForm(request.POST, instance=modified_user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=modified_user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if request.user == modified_user:
                return redirect('myauth:about-me')
            else:
                return redirect('myauth:users-list')

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'modified_user': modified_user,
        })
    
    def test_func(self):
        obj = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return self.request.user.is_staff or self.request.user == obj


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(TemplateView):
    template_name = 'myauth/logout.html'
    # http_method_names = ["get", "post", "options"]
    # def get(self, request, *args, **kwargs):
    #     logout(request)
    #     return redirect(self.next_page)


class HelloView(View):
    welcome_message = gettext_lazy('Hi mom')

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items', 5)
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(f'<h1>{self.welcome_message}</h1>'
                            f'<h2>{products_line}</h2>')
