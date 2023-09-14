from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages
from task_manager.statuses.models import Status


# Create your views here.
class IndexView(ListView):
    model = Status
    template_name = 'statuses/index.html'


class StatusCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'form.html'
    success_message = _('Status created successfully')
    success_url = reverse_lazy('statuses_list')
    fields = ['name']
    extra_context = {'title': _('Create status'), 'button': _('Create')}


class StatusUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'form.html'
    success_message = _('Status successfully changed')
    success_url = reverse_lazy('statuses_list')
    fields = ['name']
    extra_context = {'title': _('Change status'), 'button': _('Change')}


class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_message = _('Status successfully deleted')
    success_url = reverse_lazy('statuses_list')
    extra_context = {'title': _('Status deletion')}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Can't delete a status because it's in use"))
            return redirect(reverse_lazy('statuses_list'))
