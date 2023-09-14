from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages
from task_manager.labels.models import Label


# Create your views here.
class IndexView(ListView):
    model = Label
    template_name = 'labels/index.html'


class LabelCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'form.html'
    success_message = _('Label created successfully')
    success_url = reverse_lazy('labels_list')
    fields = ['name']
    extra_context = {'title': _('Create label'), 'button': _('Create')}


class LabelUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'form.html'
    success_message = _('Label successfully changed')
    success_url = reverse_lazy('labels_list')
    fields = ['name']
    extra_context = {'title': _('Change label'), 'button': _('Change')}


class LabelDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_message = _('Label successfully deleted')
    success_url = reverse_lazy('labels_list')
    extra_context = {'title': _('Label deletion')}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Can't delete a label because it's in use"))
            return redirect(reverse_lazy('labels_list'))
