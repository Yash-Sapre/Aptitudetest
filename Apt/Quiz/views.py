from django.shortcuts import render,redirect
from django.views import View
from .forms import register_user_form,add_questions_form,add_parameters_form,add_exam_form
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from .models import exam

#Written by Yash
class dashboard(View):
    def get(self,request):
        exams = exam.objects.all()
        return render(request,template_name='Quiz/dashboard.html',context={'exams':exams})

class register(View):
    form_class = register_user_form
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
    #success_url = 'Quiz/dashboard'

class logout(LogoutView):
    # success_url = reverse('Quiz/login')
    template_name = 'Quiz/logout.html'

class add_questions(View):
    form_class = add_questions_form
    def get(self,request):
        return render(request,template_name='Quiz/add_questions.html',context={'form':self.form_class})
    
    def post(self,request):
        form = self.form_class(request.POST)
    
        if form.is_valid():
            form.save()
            return redirect('Quiz:dashboard')
        else :
            messages.add_message(request,messages.INFO,'Data not entered properly')
            return redirect('Quiz:add_questions')


class add_parameters(View):
    form_class = add_parameters_form
    def get(self,request):
        return render(request,template_name='Quiz/add_parameters.html',context={'form':self.form_class})

    def post(self,request):
        form = self.form_class(request.POST)
    
        if form.is_valid():
            form.save()
            return redirect('Quiz:dashboard')
        else :
            messages.add_message(request,messages.INFO,'Data not entered properly')
            return redirect('Quiz:add_parameters')

class add_exam(View):
    form_class=add_exam_form
    def get(self,request):
        return render(request,template_name='Quiz/add_exam.html',context={'form':self.form_class})

    def post(self,request):
        form = self.form_class(request.POST)
    
        if form.is_valid():
            form.save()
            return redirect('Quiz:dashboard')
        else :
            messages.add_message(request,messages.INFO,'Data not entered properly')
            return redirect('Quiz:add_parameters')

class give_test(View):
    def get(self,request,pk):
        exam_selected = exam.objects.get(id = pk)
        
        exam_questions = exam_selected.exam_questions.all()
        return render(request,template_name='Quiz/give_test.html',context={'exam_questions':exam_questions,'exam_selected':exam_selected})

    def post(self,request,pk):
        
        exam_selected = exam.objects.get(id=pk)
        req_dict = request.POST.dict()
        req_dict.pop('csrfmiddlewaretoken')
        
        for ques_id,ans in req_dict.items() :
            #temp = models.Student_Answers.objects.create(user = request.user,exam_link=exam_instance,
            #question_link = models.Questions.objects.get(id =ques_id),student_answer = ans)
            print(ques_id)
            print(ans)

            
        # return redirect('Quiz:dashboard')

    

    