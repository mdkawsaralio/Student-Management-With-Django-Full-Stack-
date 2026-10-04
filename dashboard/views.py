from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from notice.models import Notice
from notice.forms import NoticeForm

# Create your views here.


@login_required(login_url='login')
def dashboard(request): 
    
    return render(request, 'dashboard/dashboard.html')


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
            form.save()
            return redirect('dashboard_notice')
    else:
        form=NoticeForm(initial={'author':request.user})
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
    return render(request,'dashboard/update_notice.html')



@login_required(login_url='login')
def deletenotice(request,slug):
    notice=get_object_or_404(Notice,slug=slug)
    
    if notice.author != request.user and not request.user.is_superuser:
         return HttpResponseForbidden("you can't delete it")
     
    if request.method=='POST':
         notice.delete()
         messages.success(request,'Deleted Successfully')
         return redirect('dashboard_notice')

    return redirect('dashboard_notice')
     