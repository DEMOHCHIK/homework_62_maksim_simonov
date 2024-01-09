from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from webapp.forms import TaskForm, ProjectSearchForm, ProjectForm, ProjectUserForm
from webapp.models import Task, Project
from django.urls import reverse_lazy


# -- task_views --
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object.project
        context['project'] = project
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'

    def get_success_url(self):
        project_pk = self.object.project.pk
        return reverse_lazy('webapp:project_detail', kwargs={'pk': project_pk})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_edit.html'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs.get('project_pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.kwargs['project_pk']})


# -- project_views --
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/home.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Project.objects.filter(name__icontains=query) | Project.objects.filter(description__icontains=query)
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_data = {'q': self.request.GET.get('q', '')}
        context['search_form'] = ProjectSearchForm(initial=initial_data)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['authors'] = project.authors.all()
        context['tasks'] = project.task_set.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/add_project.html'
    success_url = reverse_lazy('webapp:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.instance.authors.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_edit.html'

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('webapp:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_tasks'] = self.object.task_set.exists()
        return context


# -- users_views --

class AddAuthorView(UpdateView):
    model = Project
    form_class = ProjectUserForm
    template_name = 'add_author.html'
    context_object_name = 'project'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.pk})
