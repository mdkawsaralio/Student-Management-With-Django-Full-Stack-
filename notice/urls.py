from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('<slug:slug>',views.notice_details,name='notice_details'),
    path('all-notice/',views.all_notice,name='all_notice'),
    
]