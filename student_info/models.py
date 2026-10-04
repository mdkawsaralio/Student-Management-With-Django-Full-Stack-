from django.db import models

# Create your models here.


class Student(models.Model):
    
    name=models.CharField(max_length=70)
    father_name=models.CharField(max_length=70)
    mother_name=models.CharField(max_length=70)
    roll=models.CharField(max_length=10)
    class_name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='student/',blank=True,null=True)
    gardian_phone_number=PhoneNumberField(region="BD")
    