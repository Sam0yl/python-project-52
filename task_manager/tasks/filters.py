from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext_lazy as _
from django.forms import Select, CheckboxInput
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):

    labels = ModelChoiceFilter(label=_('Label'), queryset=Label.objects.all(), widget=Select)
    own_tasks = BooleanFilter(label=_('Just your tasks'), method='get_own_tasks', widget=CheckboxInput)

    class Meta:
        model = Task
        fields = ['status','executor','labels', 'own_tasks']
    
    def get_own_tasks(self, queryset, arg, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset