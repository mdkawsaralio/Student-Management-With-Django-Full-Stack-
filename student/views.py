from django.shortcuts import render
from notice.models import Notice

def home(request):
    notice=Notice.objects.all().order_by('-created_at')[:5]
    context={
        'notice':notice,
    }
    return render(request,'home.html',context)


