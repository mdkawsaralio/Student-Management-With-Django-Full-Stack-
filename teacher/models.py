from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



class Teacher(models.Model):
    name=models.CharField(max_length=150)
    designation=models.CharField( max_length=70)
    subject=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    phone_number=PhoneNumberField(region="BD")
    photo=models.ImageField(upload_to='teacher/',blank=True,null=True)
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name='teacher'
        verbose_name_plural='teacher'
    