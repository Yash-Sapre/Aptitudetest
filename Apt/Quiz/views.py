import reportlab.pdfgen.canvas
from django.shortcuts import render,redirect
from django.views import View
from .forms import register_user_form,add_questions_form,add_parameters_form,add_exam_form
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from .models import exam,answers, questions
from django.views.generic import DeleteView
from django.http import FileResponse
import io
import os
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart


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
        if len(exam_answers) == 0 :
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
        ''' This code checks whether the user has
        given answer to the exam and then allows access to result page with download button
        Steps:
        1)Get exam id.
        2)Retrieve answers from answer table with respective user id and exam id.
        3)If answers are found that means the user gave the exam else he did not give the exam.
        '''
        exam_selected = exam.objects.get(id=pk)
        submitted_answers = answers.objects.filter(exam__id = pk,user__id = request.user.id)
        if len(submitted_answers) > 0 :
            return render(request,template_name='Quiz/view_result.html',context={'pk':pk})
        else:
            return redirect('Quiz:dashboard')

        
        

class exam_list(View):

    def get(self,request):
        # This just checks the exam table for any exams if there are show them.
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
        '''
        The steps for calculating the parameters are :
        1)Retrieve the answers with respective user id and exam id
        2)Each question has two options the 1st option represents a parameter of 1st category and
        the 2nd option represents parameter of second category
        3)Two dictionaries have been created which stores the count of parameters
        4)Go through all answers and if option 1 selected increase count of parameter of personality_dict1
        and for option 2 count of parameter of personality_dict2
        '''
        exam_selected = exam.objects.get(id=pk)
        submitted_answers = answers.objects.filter(exam__id=pk,user__id=request.user.id)
        personality_dict1 = {'Extraversion': 0,'Sensing': 0,'Thinking': 0,'Judgement': 0}
        personality_dict2 = {'Introversion': 0,'Intuition': 0,'Feeling': 0,'Perception': 0}

        for ans in submitted_answers:
            if ans.student_answer == ans.question.answer1:
                personality_dict1[ans.question.parameter.parameter1] += 1
            else:
                personality_dict2[ans.question.parameter.parameter2] += 1

        # Calculating percentage for each parameter of first category ESTJ
        extraversion_percent = personality_dict1['Extraversion']/(personality_dict1['Extraversion']+personality_dict2['Introversion'])*100
        sensing_percent = personality_dict1['Sensing']/(personality_dict1['Sensing']+personality_dict2['Intuition'])*100
        thinking_percent = personality_dict1['Thinking']/(personality_dict1['Thinking']+personality_dict2['Feeling'])*100
        judgement_percent = personality_dict1['Judgement']/(personality_dict1['Judgement']+personality_dict2['Perception'])*100

        # Preparation for pdf and retrieving report text
        buf = io.BytesIO()
        user_id = request.user.id
        path = os.getcwd()
        with open(os.path.join(path,'ReportBase.txt'),'r') as file:
            text = file.read()
        pdf = SimpleDocTemplate(buf)
        flow = []
        styles = getSampleStyleSheet()

        # The code of text part
        paragraph_text = Paragraph(text,style=styles['Normal'])
        flow.append(paragraph_text)

        # The code of vertical bar chart
        drawing = Drawing(400, 200)
        data = [
            (extraversion_percent,sensing_percent,thinking_percent,judgement_percent),
            (100 - extraversion_percent, 100 - sensing_percent, 100 - thinking_percent, 100 -judgement_percent),
        ]
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = data
        chart.strokeColor = colors.black
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = 100
        chart.valueAxis.valueStep = 10
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.dx = 8
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.categoryNames = ['E/I', 'S/I', 'T/F','J/P']
        drawing.add(chart)
        flow.append(drawing)

        # Building the final pdf
        pdf.build(flow)
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename=f"Report {user_id}-{pk}.pdf")
    
    
