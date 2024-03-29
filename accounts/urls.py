from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterUser

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='create_user')
]