from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from .forms import TaskForm
from .models import Task


class TaskListView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class TaskDetailView(TemplateView):
    template_name = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        context['task'] = task
        return context


class TaskAddView(TemplateView):
    template_name = 'add_task.html'

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class TaskDeleteView(View):
    template_name = 'task_delete.html'

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, {'task': task})

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        task.delete()
        return redirect('home')


class TaskEditView(View):
    template_name = 'task_edit.html'

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        form = TaskForm(instance=task)
        return render(request, self.template_name, {'form': form, 'task': task})

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'task': task})