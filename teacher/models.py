from io import BytesIO
import os
from django.core.files.base import ContentFile
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image,ImageOps
from django.contrib.auth.models import User
# Create your models here.



choice= [
    ('Bangla', 'Bangla'),
    ('English', 'English'),
    ('Mathematics', 'Mathematics'),
    ('Science', 'Science'),
    ('ICT', 'ICT'),
    ('Social Science', 'Social Science'),
    ('Political Science', 'Political Science'),
    ('History', 'History'),
    ('Others', 'Others'),
]

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher',blank=True,null=True
    )
    name=models.CharField(max_length=150)
    teacher_code=models.CharField(max_length=20)
    designation=models.CharField( max_length=70)
    subject=models.CharField(choices=choice)
    address=models.CharField(max_length=150)
    phone_number=PhoneNumberField(region="BD")
    photo=models.ImageField(upload_to='teacher/',blank=True,null=True)
    
    
    def save(self,*args, **kwargs):
        if self.photo and not self.photo._committed:
            img=Image.open(self.photo)
            img = ImageOps.exif_transpose(img)  
            img = img.convert("RGB")            
            img = ImageOps.fit(img, (413, 531), Image.LANCZOS, centering=(0.5, 0.3))
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=90, optimize=True)
            filename = os.path.splitext(os.path.basename(self.photo.name))[0] + ".jpg"
            self.photo.save(filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)
   
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='teacher'
        verbose_name_plural='teacher'
    