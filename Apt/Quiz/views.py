from django.shortcuts import render
from django.views import View

#Written by Yash
class dashboard(View):
    def get(self,request):
        return render(request,template_name='Quiz/dashboard.html')

