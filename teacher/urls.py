from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>',views.teacher_details,name='teacher_details'),
    path('teacher-list/',views.teacher_list,name='teacher_list'),
]
