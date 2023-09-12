from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages
from task_manager.tasks.models import Task

# Create your views here.
class IndexView(ListView):
    model = Task
    template_name = 'tasks/index.html'

class TaskCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'form.html'
    success_message = _('Task created successfully')
    success_url = reverse_lazy('tasks_list')
    fields = ['name', 'description', 'status', 'executor']
    extra_context = {'title': _('Create task'), 'button': _('Create')}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'form.html'
    success_message = _('Task successfully changed')
    success_url = reverse_lazy('tasks_list')
    fields = ['name', 'description', 'status', 'executor']
    extra_context = {'title': _('Change task'), 'button': _('Change')}

class TaskDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_message = _('Task successfully deleted')
    success_url = reverse_lazy('tasks_list')
    extra_context = {'title': _('Task deletion'),}

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().author.id:
            messages.error(self.request, _("Task can be deleted only by its author"))
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)
