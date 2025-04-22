from django.db import models
import random

def generate_unique_user_id():
    while True:
        user_id = str(random.randint(10000000, 99999999))  # 8 أرقام
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
