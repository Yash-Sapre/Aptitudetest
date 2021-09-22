from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class questions(models.Model):
    question_text = models.CharField(max_length=120)
    answer1 = models.CharField(max_length=120)
    answer2 = models.CharField(max_length=120)
    parameter = models.ForeignKey('parameters',on_delete=CASCADE)
    def __str__(self):
        return str(self.question_text)

class parameters(models.Model):
    parameter1 = models.CharField(max_length=20)
    parameter2 = models.CharField(max_length=20)

    def __str__(self):
        return str(self.parameter1)

class exam(models.Model):
    exam_name = models.CharField(max_length=50)
    exam_questions = models.ManyToManyField(questions)
    
    def __str__(self):
        return str(self.exam_name)


class answers(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    question = models.ForeignKey('questions',on_delete=CASCADE,null=True)
    exam = models.ForeignKey('exam', on_delete=CASCADE,null=True)
    date_of_answer = models.DateTimeField(default=timezone.now)
    student_answer = models.CharField(max_length=120)

    def __str__(self) :
        return str(self.student_answer)