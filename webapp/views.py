from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from webapp.forms import TaskForm, ProjectSearchForm, ProjectForm, ProjectUserForm
from webapp.models import Task, Project
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


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


class TaskCreateView(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    permission_required = 'webapp.add_task'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().authors

    def form_valid(self, form):
        form.instance.project_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        return context


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    permission_required = 'webapp.delete_task'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().authors

    def get_success_url(self):
        project_pk = self.object.project.pk
        return reverse_lazy('webapp:project_detail', kwargs={'pk': project_pk})


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_edit.html'
    permission_required = 'webapp.change_task'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().authors

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


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/add_project.html'
    success_url = reverse_lazy('webapp:home')
    permission_required = 'webapp.add_project'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.authors.all()

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.instance.authors.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_edit.html'
    permission_required = 'webapp.change_project'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.authors.all()

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('webapp:home')
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.authors.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_tasks'] = self.object.task_set.exists()
        return context


# -- users_views --

class AddAuthorView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUserForm
    template_name = 'add_author.html'
    context_object_name = 'project'
    permission_required = 'webapp.add_user'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.authors.all()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.pk})
