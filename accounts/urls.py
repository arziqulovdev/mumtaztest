from django.urls import path
from .views import login_view, signup, confirm, logout_view

urlpatterns = [
    path("login/", login_view, name='login'),
    path('signup/', signup, name='signup'),
    path("confirm/", confirm, name='confirm'),
    path("logout/", logout_view, name='logout')
]