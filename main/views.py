from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Register, generate_unique_user_id
from django.contrib import messages
from .forms import RegisterForm
from django.core.mail import send_mail

def index(request):
    user_id = request.session.get('user_id')
    email = request.session.get('email')
    return render(request, "main/index.html", {"user_id": user_id, "email": email})

def register(request):
    if request.method == "POST":
        try:
            user = Register.objects.create(
                name=request.POST.get('name', ''),
                email=request.POST.get('email', ''),
                age=request.POST.get('age', 0),
                phone_num=request.POST.get('phone_num', ''),
                education_level=request.POST.get('education_level', '')
            )
            request.session['user_id'] = user.user_id
            request.session['email'] = user.email 
            send_mail(
                subject='رقم العضوية الخاص بك',
                message=f'مرحباً {user.name}!\nرقم العضوية الخاص بك هو: {user.user_id}',  
                from_email='islamabdenabi11@gmail.com', 
                recipient_list=[user.email],  
                fail_silently=False,  
            )

            return redirect('main')
        except Exception as e:
            print("Error:", e)

    return render(request, "main/register.html")
