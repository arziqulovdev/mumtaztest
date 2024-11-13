from django.urls import path
from .views import list, detail, result, add_question, error404, solve_test, enter_test, add_test, profile, delete_test, score

urlpatterns = [
    path("", list, name="list"),
    path("error-page/", error404, name='404'),
    path("test/<str:code>/", detail, name='detail'),
    path("test/<str:code>/result/", result, name='result'),
    path("test/<str:code>/add/", add_question, name='add_question'),
    path('test/<str:code>/solve/', solve_test, name='solve'),
    path('test/<str:code>/score/', score, name='score'),
    path('test/<str:code>/delete/', delete_test, name='delete'),
    path('profile/', profile, name='profile'),
    path("enter/", enter_test, name='enter_test'),
    path("add/", add_test, name='add_test')
]