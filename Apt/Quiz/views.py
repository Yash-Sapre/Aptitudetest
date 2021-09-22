from django.shortcuts import render,redirect
from django.views import View
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.tables import COLORED_GRID_STYLE
from .forms import register_user_form,add_questions_form,add_parameters_form,add_exam_form
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from .models import exam,answers, questions
from django.views.generic import DeleteView
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import(VerticalBarChart)

import os


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
        if len(submitted_answers) > 0 :
            return render(request,template_name='Quiz/view_result.html',context={'pk':pk})
        else:
            return redirect('Quiz:dashboard')

        
        

class exam_list(View):
    def get(self,request):
        exams = exam.objects.all()
        if len(exams) == 0:
            title = "No exams available"
        else:
            title = "List of Exams"
        return render(request,template_name='Quiz/exam_list.html',context={'exams':exams,'title':title})


class delete_exam(DeleteView):
    model = exam
    template_name = 'Quiz/delete_exam.html'


class report(View):
    def get(self,request,pk):
        exam_selected = exam.objects.get(id=pk)
        submitted_answers = answers.objects.filter(exam__id = pk,user__id = request.user.id)
        personality_dict1 = {'Extraversion': 0,'Sensing': 0,'Thinking': 0,'Judgement': 0}
        personality_dict2 = {'Introversion': 0,'Intuition': 0,'Feeling': 0,'Perception': 0}
        for ans in submitted_answers:
            if ans.student_answer == ans.question.answer1:
                personality_dict1[ans.question.parameter.parameter1] += 1
            else:
                personality_dict2[ans.question.parameter.parameter2] += 1
        drawing=Drawing(400,200)
        print(personality_dict1)
        extraversion_per=personality_dict1['Extraversion']/(personality_dict1['Extraversion']+personality_dict2['Introversion'])*100
        introversion_per=100-extraversion_per
        sensing_per=personality_dict1['Sensing']/(personality_dict1['Sensing']+personality_dict2['Intuition'])*100
        intuition_per=100-sensing_per
        thinking_per=personality_dict1['Thinking']/(personality_dict1['Thinking']+personality_dict2['Feeling'])*100
        feeling_per=100-thinking_per
        judgement_per=personality_dict1['Judgement']/(personality_dict1['Judgement']+personality_dict2['Perception'])*100
        perception_per=100-judgement_per
        data = [
            (extraversion_per,sensing_per,thinking_per,judgement_per),
            (introversion_per,intuition_per,feeling_per,perception_per)
        ]
        bc=VerticalBarChart()
        bc.x = 100
        bc.y = 100
        bc.height = 125
        bc.width = 300
        bc.data = data
        # bc.strokeColor = COLORED_GRID_STYLE.black
        buf = io.BytesIO()
        user_id = request.user.id
        pdf = canvas.Canvas(buf,pagesize='A4')
        pdf.setFont("Helvetica",14)
        #The basereport file is fixed and the text files is stored locally
        path = os.getcwd()
        with open(os.path.join(path,'ReportBase.txt'),'r') as file:
            text = file.read()

        # x and y have been set at starting position
        x = 50
        y = 770
        # lines list has been set.
        lines = ['']
        words = text.split()
        line_number = 0
        # lines list is been create with each line having limit of 78 letters
        for word in words :
            if len(lines[line_number] + ' ' + word) < 78 :
                lines[line_number] = lines[line_number] + ' ' + word
            else:
                lines.append('')
                line_number = line_number + 1
        # lines are now being printed each line has height of 15 ###Note:y can have 50 lines
        for line in lines :
            pdf.drawString(x,y,line)

            y = y - 15
        pdf.drawImage(image=bc,x=400,y=200)
        pdf.showPage()
        pdf.save()
        # buffer has been set at 0th position
        buf.seek(0)
        return FileResponse(buf, as_attachment=True,filename=f"Report {user_id}-{pk}.pdf")
    
    
