from django.shortcuts import render
from notice.models import Notice

def home(request):
    notice=Notice.objects.filter(status='published').order_by('-created_at')[:5]
    context={
        'notice':notice,
    }
    return render(request,'home.html',context)


