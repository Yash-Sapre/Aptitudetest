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
    path('give_test/<int:pk>',views.give_test.as_view(),name='give_test'),
    path('view_result/<int:pk>',views.view_result.as_view(),name='view_result'),
    # path('exam_list',views.exam_list.as_view(),name='exam_list'),
    # path('delete_exam/<int:pk>',views.delete_exam.as_view(),name='delete_exam'),
    path('report_pdf',views.report_pdf,name='report_pdf')
]