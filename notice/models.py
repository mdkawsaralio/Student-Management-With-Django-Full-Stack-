from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Notice(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,blank=True)
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
        
    def save(self,*args, **kwargs):
        if not self.slug:
            base_slug=slugify(self.title)
            slug=base_slug
            counter=2
            while Notice.objects.filter(slug=slug):
                slug=f"{self.title}-{counter}"
                counter+=1
                
            self.slug=slug
                
        super().save(*args, **kwargs)
        
        
    