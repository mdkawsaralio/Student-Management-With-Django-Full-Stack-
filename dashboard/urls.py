from django.urls import path
from . import views




urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('notice/',views.noticepage,name='dashboard_notice'),
    path('notice/create-notice/',views.addnotice,name='create_notice'),
    path('notice/update-notice/<slug:slug>',views.updatenotice,name='update_notice'),
    path('notice/delete-notice/<slug:slug>',views.updatenotice,name='delete_notice'),
    
    
]
