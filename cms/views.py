from django.contrib.auth import get_user_model, login
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView,PasswordChangeView,PasswordChangeDoneView
)
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView, UpdateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)

from .mixins import OnlyYouMixin
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm,MyPasswordChangeForm
)

UserModel = get_user_model()

class TopView(TemplateView):
    template_name = 'cms/top.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'cms/login.html'


class Logout(LogoutView):
    pass


class UserCreate(CreateView):
    form_class = UserCreateForm
    template_name = 'cms/signup.html'
    success_url = reverse_lazy('cms:top')

    def form_valid(self, form):
        print(self.request.POST['next'])
        if self.request.POST['next']=='back':
            return render(self.request,'cms/signup.html',{'form':form})
        elif self.request.POST['next']=='confirm':
            return render(self.request,'cms/signup_confirm.html',{'form':form})
        elif self.request.POST['next']=='regist':
            form.save()
            user = form.save()
            user=authenticate(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(self.get_success_url())

class signup_confirm(CreateView):
    form_class = UserCreateForm
    template_name = 'cms/signup_confirm.html'


class UserUpdate(OnlyYouMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'cms/user_update.html'

    def get_success_url(self):
        return resolve_url('cms:user_detail', pk=self.kwargs['pk'])



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception=True

    def test_func(self):
        user=self.request.user
        return user.pk==self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin,DetailView):
    model = UserModel
    template_name = 'cms/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class UserList(ListView):
    model = UserModel
    template_name = 'cms/user_list.html'


class UserDelete(OnlyYouMixin, DeleteView):
    model = UserModel
    template_name = 'cms/user_delete.html'
    success_url = reverse_lazy('cms:top')

class PasswordChange(PasswordChangeView):
    form_class=MyPasswordChangeForm
    success_url=reverse_lazy('cms:password_change_done')
    template_name='cms/password_change_form.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワードを変更しました"""
    template_name='cms/password_change_done.html'