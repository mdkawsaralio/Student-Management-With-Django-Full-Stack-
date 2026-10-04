from django.shortcuts import render
from .models import Notice
from django.shortcuts import get_object_or_404

# Create your views here.


def notice_details(request,slug):
    post=Notice.objects.get(slug=slug)
    context={
        'post':post,
    }
    return render(request, 'notice/notice_details.html',context)



def all_notice(request):
    post=Notice.objects.filter(status='published')
    
    context={
        'post':post,
    }
    return render (request, 'notice/all_notice.html',context)


