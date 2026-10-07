from django.contrib import admin
from .models import Student,Exam,Result,Subject

# Register your models here.



class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_id']

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(Subject,SubjectAdmin)
