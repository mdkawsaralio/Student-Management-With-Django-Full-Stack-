from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render,redirect
from notice.models import Notice
from notice.forms import NoticeForm
from student_info.models import Student,Result,Exam
from student_info.forms import StudentForm,ResultFormset,UpdateResultFormset
from teacher.models import Teacher
from teacher.forms import TeacherForm
from django.db.models import Q
from django.contrib.auth.models import User
from account.forms import UserCreateForm
from django.contrib.auth.models import Group
from account.decorators import role_required, user_in_group


# Create your views here.


@role_required('Admin', 'Teacher', 'Student')
def dashboard(request): 
    teacher_count=Teacher.objects.all().count()
    student_count=Student.objects.all().count()
    context={
        'teacher_count':teacher_count,
        'student_count':student_count
    }
    return render(request, 'dashboard/dashboard.html',context)


@role_required('Admin','Teacher','Student')
def noticepage(request):
    notice=Notice.objects.all()
    context={
        'notice':notice
    }
    return render(request,'dashboard/dashboard_notice.html', context)



@role_required('Admin','Teacher')
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
        
        
        
@role_required('Admin','Teacher')
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



@role_required('Admin','Teacher')
def deletenotice(request,slug):
    notice=get_object_or_404(Notice,slug=slug)
    
    if notice.author != request.user and not request.user.is_superuser:
         return HttpResponseForbidden("you can't delete it")
     
    notice.delete()
    messages.success(request,'Deleted Successfully')
    return redirect('dashboard_notice')



@role_required('Admin','Teacher')
def student_list(request):
    student=Student.objects.all()
    context={
        'student':student
    }
    return render(request,'dashboard/dashboard_student.html',context)



@role_required('Admin','Teacher')
def student_details(request,id):
    student=Student.objects.get(id=id)
    exam=Exam.objects.filter(result__student=student).distinct()
    context={
        'student':student,
        'exam':exam
    }
    return render(request,'dashboard/dashboard_student_details.html',context)



@role_required('Admin','Teacher')
def student_result(request,student_id,exam_id):
    student=get_object_or_404(Student,id=student_id)
    exam=get_object_or_404(Exam,id=exam_id)
    result=Result.objects.filter(student=student,exam=exam)
    total_mark=sum(i.marks for i in result)
    average_mark=total_mark/len(result) if result else 0
    
    if average_mark >=80:
        cgpa="A+"
    elif average_mark >=70:
        cgpa="A"
    elif average_mark >=60:
        cgpa="A-"
    elif average_mark >=50:
        cgpa="B"
    elif average_mark>=40:
        cgpa="C"
    elif average_mark>=33:
        cgpa="D"
    else:
        cgpa="F"
    
    context={
        'student':student,
        'exam':exam,
        'result':result,
        'cgpa':cgpa
    }
    return render(request,'dashboard/student_result.html',context)
    
    


@role_required('Admin','Teacher')
def create_student(request):
    if request.method=="POST":
        user=UserCreateForm(request.POST)
        student=StudentForm(request.POST,request.FILES)
        result=ResultFormset(request.POST,prefix='result')
        if student.is_valid() and result.is_valid() and user.is_valid():
            with transaction.atomic():
                user=user.save()
                user.groups.add(Group.objects.get(name='Student'))
                student=student.save(commit=False)
                student.user=user
                student.save()
                result.instance=student
                result.save()
                return redirect('dashboard_student')
    else:
        student=StudentForm()
        result=ResultFormset(prefix='result')
        user=UserCreateForm()
    return render(request,'dashboard/create_student.html',{'student':student,'result':result,'user':user})



@role_required('Admin','Teacher')
def update_student(request,id):
    student= get_object_or_404(Student,id=id)
    if request.method=="POST":
        form=StudentForm(request.POST,request.FILES,instance=student)
        result=UpdateResultFormset(request.POST,instance=student,prefix='result')
        
        if form.is_valid() and result.is_valid() :
            student=form.save()
            result.instance=student
            result.save()
            return redirect('dashboard_student')
    else:
        form=StudentForm(instance=student)
        result=UpdateResultFormset(instance=student, prefix='result')
        
    return render(request,'dashboard/update_student.html',{'form':form,'result':result})



@role_required('Admin','Teacher')
def delete_student(request,id):
    student=get_object_or_404(Student,id=id)
    
    if student:
        student.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('dashboard_student')

    else:
        messages.error(request,'No Data Found')
    return redirect('dashboard_student')


@role_required('Admin','Teacher')
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


@role_required('Admin','Teacher')
def teacher_list(request):
    teacher=Teacher.objects.all()
    return render(request,'dashboard/dashboard_teacher.html',{'teacher':teacher})


@role_required('Admin',)
def create_teacher(request):
    if request.method=='POST':
        user=UserCreateForm(request.POST)
        form=TeacherForm(request.POST,request.FILES)
        if form.is_valid() and user.is_valid():
            with transaction.atomic():
                user=user.save()
                user.groups.add(Group.objects.get(name='Teacher'))
                form=form.save(commit=False)
                form.user=user
                form.save()
                return redirect('dashboard_teacher')
    else:
        form=TeacherForm()
        user=UserCreateForm()
        
    return render(request,'dashboard/create_teacher.html',{'form':form,'user':user})

@role_required('Admin',)
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
        


@role_required('Admin',)
def delete_teacher(request,id):
    teacher=get_object_or_404(Teacher,id=id)
    
    if teacher:
        teacher.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('dashboard_teacher')

    else:
        messages.error(request,'No Data Found')
    return redirect('dashboard_teacher')


@role_required('Admin',)
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



@role_required('Admin',)
def user_list(request):
    users=User.objects.all()
    return render(request,'dashboard/dashboard_user.html',{'users':users})


@role_required('Admin',)
def create_user(request):
    if request.method=='POST':
        form=UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_user')
    else:
        form=UserCreateForm()
        
    return render(request,'dashboard/create_user.html',{'form':form})

@role_required('Admin',)
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
        


@role_required('Admin',)
def delete_user(request,id):
    user=get_object_or_404(User,id=id)
    
    if user:
        user.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('dashboard_user')

    else:
        messages.error(request,'No Data Found')
    return redirect('dashboard_user')


@role_required('Admin',)
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