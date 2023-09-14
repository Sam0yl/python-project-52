from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from task_manager.users.forms import CustomUserCreationForm, CustomUserChangeForm


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'users/index.html'


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'form.html'
    success_message = _('User created successfully')
    success_url = reverse_lazy('login')
    extra_context = {'title': _('Registration'), 'button': _('Sign up')}


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
    template_name = 'form.html'
    success_message = _('User successfully changed')
    success_url = reverse_lazy('users_list')
    extra_context = {'title': _('User change'), 'button': _('Change')}


class UserDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    success_message = _('User successfully deleted')
    success_url = reverse_lazy('users_list')
    extra_context = {'title': _('User deletion')}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Can't delete a user because it's in use"))
            return redirect(reverse_lazy('statuses_list'))
