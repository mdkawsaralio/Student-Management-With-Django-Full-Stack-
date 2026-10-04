from django.contrib import admin
from .models import Notice
from django.utils.text import slugify
# Register your models here.


class NoticeAdim(admin.ModelAdmin):
    list_display=('title','author','status','created_at','updated_at')
    list_filter=('title','author','status')
    readonly_fields = ('slug','created_at','updated_at','author')
    
    
    def save_model(self, request, obj, form, change):
        
        if not obj.author_id:
            obj.author = request.user
            
        if not obj.slug:
            obj.save()
            obj.slug=f"{slugify(obj.title)}-{obj.id}"
            obj.save()
            
        return super().save_model(request, obj, form, change)

    
admin.site.register(Notice,NoticeAdim)