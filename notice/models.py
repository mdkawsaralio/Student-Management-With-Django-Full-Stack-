from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Notice(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    short_description=models.TextField(max_length=200)
    description=models.TextField(max_length=1500)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=[
        ('published', 'Published'),
        ('draft', 'Draft'),
    ],default='draft')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Notice'
        verbose_name_plural='Notice'
        
    