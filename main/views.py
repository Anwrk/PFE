from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Register, generate_unique_user_id, Event
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
                subject='رقم عضويتك',
                message = (f"""مرحباً {user.name} 🌟،

            سعدنا بانضمامك إلينا!

             {user.user_id}
             
            .هذا هو رقم عضويتك. يمكنك استخدامه للمشاركة في المسابقات 

            .✨نتمنى لك تجربة رائعة معنا 
        """
                ),
                from_email='abdislem553@gmail.com',
                recipient_list=[user.email],
                fail_silently=False,
            )


            return redirect('main')
        except Exception as e:
            print("Error:", e)

    return render(request, "main/register.html")

def events(request):
    events = Event.objects.all().order_by('title')  
    return render(request, 'main/events.html', {'events': events})

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'main/event_details.html', {'event': event})
