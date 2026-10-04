from django import forms
from .models import Notice



class NoticeForm(forms.ModelForm):
    
    class Meta:
        model=Notice
        exclude = ['slug', 'created_at', 'updated_at','author']
        
        
        
        