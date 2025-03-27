from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


# Custom login view for the app
class CustomLoginView(LoginView):
    template_name = 'base/login.html'  # The template to use for login page
    fields = '__all__'  # All fields of the form will be included
    redirect_authenticated_user = True  # Redirect already logged-in users to tasks page

    def get_success_url(self):
        # Redirect to task list page after successful login
        return reverse_lazy('tasks')


# Register page where users can create an account
class RegisterPage(FormView):
    template_name = 'base/register.html'  # Template for the registration page
    form_class = UserCreationForm  # Use the built-in UserCreationForm
    redirect_authenticated_user = True  # Redirect logged-in users to tasks page
    success_url = reverse_lazy('tasks')  # Redirect to task list page after successful registration

    def form_valid(self, form):
        user = form.save()  # Save the form to create a new user
        if user is not None:
            login(self.request, user)  # Log in the newly created user
        return super(RegisterPage, self).form_valid(form)  # Redirect on successful form submission

    def get(self, *args, **kwargs):
        # If user is already authenticated, redirect to tasks page
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# Task list view that displays all tasks for the logged-in user
class TaskList(LoginRequiredMixin, ListView):
    model = Task  # Task model
    template_name = 'base/task_list.html'  # Template for displaying the task list
    context_object_name = 'tasks'  # Context variable to hold the task list

    def get_queryset(self):
        # Filter tasks based on the logged-in user and search input
        queryset = Task.objects.filter(user=self.request.user)
        search_input = self.request.GET.get('search-area', '').strip()  # Get search input from query parameters

        if search_input:
            queryset = queryset.filter(title__icontains=search_input)  # Filter tasks by title if search input is provided

        return queryset

    def get_context_data(self, **kwargs):
        # Add extra context to the template (completed tasks percentage and task count)
        context = super().get_context_data(**kwargs)
        
        total_tasks = Task.objects.filter(user=self.request.user).count()  # Total number of tasks for the user
        completed_tasks = Task.objects.filter(user=self.request.user, complete=True).count()  # Number of completed tasks

        # Calculate the completed percentage
        if total_tasks > 0:
            completed_percentage = (completed_tasks / total_tasks) * 100
        else:
            completed_percentage = 0  # Avoid division by zero

        # Add calculated data to context
        context['completed_percentage'] = completed_percentage
        context['count'] = total_tasks - completed_tasks  # Incomplete tasks count
        context['search_input'] = self.request.GET.get('search-area', '')  # Retain search input value in the context

        return context


# Task detail view to show details of a specific task
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task  # Task model
    context_object_name = 'task'  # Context variable for the task
    template_name = 'base/task.html'  # Template for task details page

    def get_queryset(self):
        # Filter tasks based on the logged-in user
        return Task.objects.filter(user=self.request.user)


# Task creation view to allow users to create new tasks
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task  # Task model
    fields = ['title', 'description', 'complete', 'due_date']  # Fields to be included in the task form (including due date)
    success_url = reverse_lazy('tasks')  # Redirect to task list page after successful creation

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the task to the logged-in user
        return super(TaskCreate, self).form_valid(form)

    def get_form(self, form_class=None):
        # Customise the task form to include a date picker for the due date
        form = super(TaskCreate, self).get_form(form_class)
        form.fields['due_date'].widget.attrs.update({'type': 'date'})  # Add a date picker to the due_date field
        return form


# Task update view to allow users to edit existing tasks
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task  # Task model
    fields = ['title', 'description', 'complete', 'due_date']  # Fields to be included in the task form (including due date)
    success_url = reverse_lazy('tasks')  # Redirect to task list page after successful update

    def get_queryset(self):
        # Filter tasks based on the logged-in user to prevent editing others' tasks
        return Task.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        # Customise the task form to include a date picker for the due date
        form = super(TaskUpdate, self).get_form(form_class)
        form.fields['due_date'].widget.attrs.update({'type': 'date'})  # Add a date picker to the due_date field
        return form


# Task delete view to allow users to delete tasks
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task  # Task model
    context_object_name = 'task'  # Context variable for the task
    success_url = reverse_lazy('tasks')  # Redirect to task list page after successful deletion

    def get_queryset(self):
        # Filter tasks based on the logged-in user to prevent deletion of other's tasks
        return Task.objects.filter(user=self.request.user)
