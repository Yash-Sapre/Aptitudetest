from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name = 'quiz'

urlpatterns = [
    path('',views.dashboard.as_view(),name='dashboard'),
]