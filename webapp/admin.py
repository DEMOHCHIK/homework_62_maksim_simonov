from django.contrib import admin
from .models import Status, Type, Task, Project


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'add_time', 'edit_time']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date']
