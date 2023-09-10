from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.users.forms import CustomUserCreationForm, CustomUserChangeForm


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'users/index.html'

class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_message = _('User created successfully')
    success_url = reverse_lazy("login")


class CustomLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, _('You are not authorised! Please log in.'))
            self.handle_no_permission()

        elif request.user.id != self.get_object().id:
            messages.error(self.request, _("You don't have permission to modify another user."))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)
            

class UserUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_message = _('User successfully changed')
    success_url = reverse_lazy("users_list")

class UserDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = _('User successfully deleted')
    success_url = reverse_lazy("users_list")
    

    
