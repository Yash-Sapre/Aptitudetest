from django.shortcuts import render,redirect
from django.views import View
from .forms import register_user_form,add_questions_form,add_parameters_form,add_exam_form
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from .models import exam,answers, questions
from django.views.generic import DeleteView

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


class logout(LogoutView):
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
        exam_answers = answers.objects.filter(exam__id = pk,user__id = request.user.id)
        if(len(exam_answers) == 0):
            exam_questions = exam_selected.exam_questions.all()
            return render(request,template_name='Quiz/give_test.html',context={'exam_questions':exam_questions,'exam_selected':exam_selected})    
        else:   
            return redirect('Quiz:dashboard')
        
    def post(self,request,pk):
        exam_selected = exam.objects.get(id=pk)
        req_dict = request.POST.dict()
        req_dict.pop('csrfmiddlewaretoken')
        for ques_id,ans in req_dict.items() :
            temp = answers.objects.create(user = request.user,exam=exam_selected,question = questions.objects.get(id =ques_id),student_answer = ans)
        return redirect('Quiz:dashboard')


class view_result(View):
    def get(self,request,pk):
        exam_selected = exam.objects.get(id=pk)
        submitted_answers = answers.objects.filter(exam__id = pk,user__id = request.user.id)
        if(len(submitted_answers)> 0):
            personality_dict = {'Extraversion':'E','Introversion':'I','Sensing':'S','Intuition':'N','Thinking':'T','Feeling':'F','Judgement':'J','Perception':'P'}
            personality_dict1 = {'Extraversion':0,'Sensing':1,'Thinking':2,'Judgement':3}
            personality_dict1_lst = ['Extraversion','Sensing','Thinking','Judgement']
            personality_dict2 = {'Introversion':0,'Intuition':1,'Feeling':2,'Perception':3}
            personality_dict2_lst = ['Introversion','Intuition','Feeling','Perception']

            parameters_list=[]
            
            para_num_list=[0,0,0,0]
            final_parameters=['Half Extraversion half Introversion','Half S half I','Half Thinking half feeling','Half Judgement half perception']
            for ans in submitted_answers:
                if ans.student_answer == ans.question.answer1:
                    parameters_list.append(personality_dict[ans.question.parameter.parameter1])
                    # print(personality_dict1[ans.question.parameter.parameter1])
                    para_num_list[personality_dict1[ans.question.parameter.parameter1]] += 1

                else:
                    parameters_list.append(personality_dict[ans.question.parameter.parameter2])
                    para_num_list[personality_dict2[ans.question.parameter.parameter2]] -= 1
                parameter_word = ''.join(parameters_list)

            index=0
            for value in para_num_list:

                if value > 0 :
                    final_parameters[index] = personality_dict1_lst[index]
                elif value < 0 :
                    final_parameters[index] = personality_dict2_lst[index]
                index=index+1  

            return render(request,template_name='Quiz/view_result.html',context={'lst':final_parameters,'lst2':parameters_list})                
        else:
            return redirect('Quiz:dashboard')

class exam_list(View):
    def get(self,request):
        exams = exam.objects.all()
        if (len(exams) == 0):
            title="No exams available"
        else:
            title = "List of Exams"
        return render(request,template_name='Quiz/exam_list.html',context={'exams':exams,'title':title})

class delete_exam(DeleteView):
    model = exam
    template_name = 'Quiz/delete_exam.html'
    