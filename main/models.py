from django.db import models
import random
import secrets 
from django.utils.text import slugify

def generate_unique_user_id():
    while True:
        user_id = str(secrets.token_hex(8))  # 8 أرقام
        if not Register.objects.filter(user_id=user_id).exists():
            return user_id

class Register(models.Model):
    user_id = models.CharField(max_length=8, default=generate_unique_user_id, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    phone_num = models.CharField(max_length=15)
    education_level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user_id} - {self.name}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()  
    image = models.ImageField(upload_to='photos/%y/%m/%d/')
    slug = models.CharField(max_length=200, blank=True)  # تغيير هنا: استخدم CharField بدون unique وبدون slugify

    def save(self, *args, **kwargs):
        if not self.slug:  # إذا لم يكن هناك slug محدد، استخدم العنوان كـ slug
            self.slug = self.title
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title    
