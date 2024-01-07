from accounts.forms import MyUserCreationForm
from django.shortcuts import reverse, render, redirect
from django.contrib.auth import login, get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy


class RegisterUser(CreateView):
    model = get_user_model()
    form_class = MyUserCreationForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('webapp:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if not next_page:
            next_page = self.request.POST.get('next')
        if not next_page:
            next_page = reverse('webapp:home')

        return next_page

