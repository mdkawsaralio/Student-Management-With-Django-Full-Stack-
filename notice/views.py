from django.shortcuts import render
from .models import Notice
from django.shortcuts import get_object_or_404
from django.db.models import Q

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




def notice_search(request):
    keyword=request.GET.get('keyword').strip()
    if keyword:
        notice=Notice.objects.filter(Q(title__icontains=keyword)|Q(description__icontains=keyword)|Q(short_description__icontains=keyword),status='published')
    else:
        notice=Notice.objects.none()
    
    context={
                'keyword':keyword,
                'notice':notice
            }
    
    return render(request, 'notice/search.html',context)


