from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name = 'Quiz'

urlpatterns = [
    path('dashboard',views.dashboard.as_view(),name='dashboard'),
    path('register' ,views.register.as_view() ,name='register'),
    path('login'    ,views.login.as_view()    ,name='login'),
    path('logout'   ,views.logout.as_view()   ,name='logout'),

]