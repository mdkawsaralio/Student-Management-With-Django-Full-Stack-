from django.contrib import admin
from .models import Teacher
# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
    list_display=('name','designation','subject','address',)
    list_filter=('name','designation','subject','address')
    search_fields=('name','subject','designation')
    
admin.site.register(Teacher,TeacherAdmin)