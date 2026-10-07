from io import BytesIO
import os
from django.core.files.base import ContentFile
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image,ImageOps
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name='student',blank=True,null=True
        )
    name=models.CharField(max_length=70)
    father_name=models.CharField(max_length=70)
    mother_name=models.CharField(max_length=70)
    roll=models.CharField(max_length=10)
    class_name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='student/',blank=True,null=True)
    gardian_phone_number=PhoneNumberField(region="BD")
    address=models.CharField(max_length=150)
    
    
    def __str__(self):
        return self.name
    
    
    def save(self,*args, **kwargs):
            if self.image and not self.image._committed:
                img=Image.open(self.image)
                img = ImageOps.exif_transpose(img)  
                img = img.convert("RGB")            
                img = ImageOps.fit(img, (413, 531), Image.LANCZOS, centering=(0.5, 0.3))
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=90, optimize=True)
                filename = os.path.splitext(os.path.basename(self.image.name))[0] + ".jpg"
                self.image.save(filename, ContentFile(buffer.getvalue()), save=False)
    
            super().save(*args, **kwargs)
            
    
    class Meta:
        verbose_name='student'
        verbose_name_plural='student'
        
        
        
class Subject(models.Model):
    name=models.CharField( max_length=80)
    subject_id=models.CharField(max_length=10)
    
    
    def __str__(self):
         return self.name
     


class Exam(models.Model):
    exam=models.CharField(choices=[('mid','Mid'),('final','Final')],max_length=6)
    year=models.IntegerField()
    
    def __str__(self):
         return f"{self.exam}-{self.year}"


class Result(models.Model):
    student=models.ForeignKey("Student", on_delete=models.CASCADE,related_name='result')
    exam=models.ForeignKey('Exam',on_delete=models.CASCADE,related_name='result')
    subject=models.ForeignKey('Subject',on_delete=models.CASCADE,related_name='result')
    marks=models.FloatField()
    GPA=models.CharField(max_length=3)
    
    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['student', 'exam', 'subject'],
            name='unique_student_exam_subject'
        )
    ]
    
    def calculate_gpa(self):
        if self.marks>=80:
            return 'A+'
        elif self.marks>=70:
            return 'A'
        elif self.marks>=60:
            return 'A-'
        elif self.marks>=50:
            return 'B'
        elif self.marks>=40:
            return 'C'
        elif self.marks>=33:
            return 'D'
        else:
            return 'F'
        
        
    def save(self,*args, **kwargs):
        self.GPA=self.calculate_gpa()
        super().save(*args, **kwargs)
    
    
    def __str__(self):
         return f"{self.student} {self.exam}"
        
    