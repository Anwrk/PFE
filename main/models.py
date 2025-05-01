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
    user_id = models.CharField(max_length=20, default=generate_unique_user_id, unique=True)
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



class Form(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    TEXT = 'text'
    PARAGRAPH = 'paragraph'
    CHOICE = 'choice'        # اختيار من متعدد (راديو)
    DROPDOWN = 'dropdown'    # قائمة منسدلة
    MULTICHOICE = 'multichoice'  # Checkboxes

    QUESTION_TYPES = [
        (TEXT, 'Short Answer'),
        (PARAGRAPH, 'Paragraph'),
        (CHOICE, 'Multiple Choice'),
        (DROPDOWN, 'Dropdown'),
        (MULTICHOICE, 'Checkboxes'),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    choices = models.TextField(blank=True, help_text="Comma-separated choices (only for choice/dropdown/multichoice)")

    def __str__(self):
        return self.text


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()


