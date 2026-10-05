from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from teacher.views import teacher_details
from notice.views import notice_details


urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('notice/',views.noticepage,name='dashboard_notice'),
    path('notice/details/<slug:slug>',notice_details,name='notice_details'),
    path('notice/create-notice/',views.addnotice,name='create_notice'),
    path('notice/update-notice/<slug:slug>',views.updatenotice,name='update_notice'),
    path('notice/delete-notice/<slug:slug>',views.deletenotice,name='delete_notice'),
    
    
    path('student/',views.student_list,name='dashboard_student'),
    path('student/details/<int:id>',views.student_details,name='student_details'),
    path('student/create-student/',views.create_student,name='create_student'),
    path('student/update-student/<int:id>',views.update_student,name='update_student'),
    path('student/delete-student/<int:id>',views.delete_student,name='delete_student'),
    path('student/<int:student_id>/student-result/<int:exam_id>',views.student_result,name='student_result'),   
        
    path('teacher/',views.teacher_list,name='dashboard_teacher'),
    path('teacher/details/<int:id>',teacher_details,name='teacher_details'),
    path('teacher/create-teacher/',views.create_teacher,name='create_teacher'),
    path('teacher/update-teacher/<int:id>',views.update_teacher,name='update_teacher'),
    path('teacher/delete-teacher/<int:id>',views.delete_teacher,name='delete_teacher'),
    
    
    path('user/',views.user_list,name='dashboard_user'),
    path('user/create-user/',views.create_user,name='create_user'),
    path('user/update-user/<int:id>',views.update_user,name='update_user'),
    path('user/delete-user/<int:id>',views.delete_user,name='delete_user'),
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)