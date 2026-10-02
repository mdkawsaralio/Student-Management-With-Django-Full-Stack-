from django.shortcuts import render
from .models import Teacher
# Create your views here.


def teacher_list(request):
    teacher=Teacher.objects.all().order_by('subject','name')
    context={
        'teacher':teacher,
    }
    return render(request,'teacher/teacher.html',context)


def teacher_details(request,pk):
    teacher=Teacher.objects.get(pk=pk)
    context={
        'teacher':teacher
    }
    return render(request,'teacher/teacher_details.html',teacher)