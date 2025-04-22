from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Register
import random

def index(request):
    return render(request, "main/index.html")

def register(request):
    if request.method == "POST":
        try:
            Register.objects.create(
                name=request.POST.get('name',''),
                email=request.POST.get('email', ''),
                age=request.POST.get('age', 0),
                phone_num=request.POST.get('phone_num', ''),
                education_level=request.POST.get('education_level', '')
            )
        except Exception as e:
            pass

    return render(request, "main/register.html")
