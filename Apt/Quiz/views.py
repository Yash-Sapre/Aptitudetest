from django.shortcuts import render,redirect
from django.views import View
from Quiz import forms
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy

#Written by Yash
class dashboard(View):
    
    def get(self,request):
        
        return render(request,template_name='Quiz/dashboard.html')

class register(View):
    form_class = forms.register_user_form
    template_name = 'Quiz/register.html'

    def get(self,request):

        return render(request,template_name = 'Quiz/register.html',context = {'form':self.form_class})
   
    def post(self,request):

        form = self.form_class(request.POST)

        if form.is_valid():

            form.save()
            return redirect('Quiz:login')

        else :

            messages.add_message(request,messages.INFO,'Data not entered properly')
            return redirect('Quiz:register')

class login(LoginView):
    template_name = 'Quiz/login.html'
    redirect_field_name = reverse('Quiz:dashboard')

class logout(LogoutView):
    success_url = 'Quiz/dashboard'