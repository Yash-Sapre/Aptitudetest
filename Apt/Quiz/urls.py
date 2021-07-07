from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name = 'Quiz'

urlpatterns = [
    path('dashboard',views.dashboard.as_view(),name='dashboard'),
    path('register' ,views.register.as_view(),name='register'),
    path('login'    ,views.login.as_view(),name='login'),
    path('logout'   ,views.logout.as_view(),name='logout'),
    path('add_questions',views.add_questions.as_view(),name='add_questions'),
    path('add_parameters',views.add_parameters.as_view(),name='add_parameters'),
    path('add_exam',views.add_exam.as_view(),name='add_exam'),
    path('give_test',views.givetest,name='give_test'),
]