from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from notice.models import Notice
from notice.forms import NoticeForm
from student_info.models import Student,Result,Exam
from student_info.forms import StudentForm
from teacher.models import Teacher
from teacher.forms import TeacherForm
from django.db.models import Q
from django.contrib.auth.models import User
from account.forms import UserCreateForm

# Create your views here.


@login_required(login_url='login')
def dashboard(request): 
    teacher_count=Teacher.objects.all().count()
    student_count=Student.objects.all().count()
    context={
        'teacher_count':teacher_count,
        'student_count':student_count
    }
    return render(request, 'dashboard/dashboard.html',context)


@login_required(login_url='login')
def noticepage(request):
    notice=Notice.objects.all()
    context={
        'notice':notice
    }
    return render(request,'dashboard/dashboard_notice.html', context)



@login_required(login_url='login')
def addnotice(request):
    if request.method=='POST':
        form=NoticeForm(request.POST)
        if form.is_valid():
            notice= form.save(commit=False)
            notice.author=request.user
            notice.save()
            return redirect('dashboard_notice')
    else:
        form=NoticeForm()
    return render(request,'dashboard/create_notice.html',{'form':form})
        
        
        
@login_required(login_url='login')
def updatenotice(request,slug):
    notice=get_object_or_404(Notice,slug=slug)
    
    if notice.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can't edit this notice.")
    if request.method=='POST':
        form=NoticeForm(request,instance=notice)
        if form.is_valid():
            form.save()
            return redirect('dashboard_notice')
    else:
        form=NoticeForm(instance=notice)
    return render(request,'dashboard/update_notice.html',{'form':form})



@login_required(login_url='login')
def deletenotice(request,slug):
    notice=get_object_or_404(Notice,slug=slug)
    
    if notice.author != request.user and not request.user.is_superuser:
         return HttpResponseForbidden("you can't delete it")
     
    notice.delete()
    messages.success(request,'Deleted Successfully')
    return redirect('dashboard_notice')



@login_required(login_url='login')
def student_list(request):
    student=Student.objects.all()
    context={
        'student':student
    }
    return render(request,'dashboard/dashboard_student.html',context)




@login_required(login_url='login')
def student_details(request,id):
    student=Student.objects.get(id=id)
    context={
        'student':student
    }
    return render(request,'dashboard/dashboard_student_details.html',context)



@login_required(login_url='login')
def student_result(request,student_id,exam_id):
    student=get_object_or_404(Student,id=student_id)
    exam=get_object_or_404(Exam,id=exam_id)
    result=Result.objects.filter(student=student,exam=exam)
    context={
        'student':student,
        'exam':exam,
        'result':result
    }
    return render(request,'dashboard/student_result.html',context)
    
    


@login_required(login_url='login')
def create_student(request):
    if request.method=="POST":
        student=StudentForm(request.POST)
        if student.is_valid():
            student.save()
            return redirect('dashboard_student')
    else:
        student=StudentForm()
    return render(request,'dashboard/create_student.html',{'student':student})



@login_required(login_url='login')
def update_student(request,id):
    student= get_object_or_404(Student,id=id)
    if request.method=="POST":
        form=StudentForm(request,instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard_student')
    
    else:
        form=StudentForm(instance=student)
        
    return render(request,'dashboard/update_student.html',{'form':form})



@login_required(login_url='login')
def delete_student(request,id):
    student=get_object_or_404(Student,id=id)
    
    if student:
        student.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('dashboard_student')

    else:
        messages.error(request,'No Data Found')
    return redirect('dashboard_student')


@login_required(login_url='login')
def search_student(request):
    keyword=request.GET.get('keyword').strip()
    
    if keyword:
        student=Student.objects.filter(Q(name__icontains=keyword)|Q(roll__icontains=keyword)|Q(father_name__icontains=keyword)|Q(mother_name__icontains=keyword))
    
    else:
        student=Student.objects.none()
    
    context={
        'student':student,
        'keyword':keyword
    }
    return render(request,'dashboard/dashboard_student.html',context)



@login_required(login_url='login')
def teacher_list(request):
    teacher=Teacher.objects.all()
    return render(request,'dashboard/dashboard_teacher.html',{'teacher':teacher})


@login_required(login_url='login')
def create_teacher(request):
    if request.method=='POST':
        form=TeacherForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard_teacher')
    else:
        form=TeacherForm()
        
    return render(request,'dashboard/create_teacher.html',{'form':form})


def update_teacher(request,id):
    teacher=get_object_or_404(Teacher,id=id)
    if request.method=='POST':
        form=TeacherForm(request.POST,instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('database_teacher')
        
    else:
        form=TeacherForm(instance=teacher)
    return render(request, 'dashboard/update_teacher.html',{'form':form})
        


@login_required(login_url='login')
def delete_teacher(request,id):
    teacher=get_object_or_404(Teacher,id=id)
    
    if teacher:
        teacher.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('dashboard_teacher')

    else:
        messages.error(request,'No Data Found')
    return redirect('dashboard_teacher')


@login_required(login_url='login')
def search_teacher(request):
    keyword=request.GET.get('keyword').strip()
    
    if keyword:
        teacher=Teacher.objects.filter(Q(name__icontains=keyword)|Q(teacher_code__icontains=keyword)|Q(subject__icontains=keyword))
    
    else:
        teacher=Teacher.objects.none()
    
    context={
        'teacher':teacher,
        'keyword':keyword
    }
    return render(request,'dashboard/dashboard_teacher.html',context)





@login_required(login_url='login')
def user_list(request):
    user=User.objects.all()
    return render(request,'dashboard/dashboard_user.html',{'user':user})


@login_required(login_url='login')
def create_user(request):
    if request.method=='POST':
        form=UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_user')
    else:
        form=UserCreateForm()
        
    return render(request,'dashboard/create_user.html',{'form':form})

@login_required(login_url='login')
def update_user(request,id):
    user=get_object_or_404(User,id=id)
    if request.method=='POST':
        form=UserCreateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('database_user')
        
    else:
        form=UserCreateForm(instance=user)
        
    return render(request,'dashboard/update_user.html',{'form':form})
        


@login_required(login_url='login')
def delete_user(request,id):
    user=get_object_or_404(User,id=id)
    
    if user:
        user.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('dashboard_user')

    else:
        messages.error(request,'No Data Found')
    return redirect('dashboard_user')


@login_required(login_url='login')
def search_user(request):
    keyword=request.GET.get('keyword').strip()
    
    if keyword:
       user=User.objects.filter(Q(username__icontains=keyword)|Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
    
    else:
        user=User.objects.none()
    
    context={
        'user':user,
        'keyword':keyword
    }
    return render(request,'dashboard/dashboard_user.html',context)