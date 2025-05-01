from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Register, generate_unique_user_id, Event, Form, Question, Response, Answer
from django.contrib import messages
from .forms import RegisterForm, DynamicForm, FormCreateForm, QuestionFormSet
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


def form_list(request):
    forms = Form.objects.all()
    return render(request, 'main/form_list.html', {'forms': forms})

def answers_list(request):
    forms = Form.objects.all()
    return render(request, 'main/answers_list.html', {'forms': forms})

def form_detail(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('verify_user_id', form_id=form_id)
    questions = Question.objects.filter(form=form_instance)

    if request.method == 'POST':
        form = DynamicForm(questions, request.POST)
        if form.is_valid():
            response = Response.objects.create(form=form_instance, user_id="anonymous")  # أو عدل حسب المستخدم
            for question in questions:
                answer_text = form.cleaned_data[str(question.id)]
                if isinstance(answer_text, list):  # لو checkboxes
                    answer_text = ', '.join(answer_text)
                Answer.objects.create(response=response, question=question, text=answer_text)
            return redirect('form_list')
    else:
        form = DynamicForm(questions)

    return render(request, 'main/form_detail.html', {
        'form_instance': form_instance,
        'form': form
    })

def form_responses(request, form_id):
    form_instance = get_object_or_404(Form, pk=form_id)

    responses = Response.objects.filter(form=form_instance).prefetch_related('answers__question')

    context = {
        'form': form_instance,
        'responses': responses,
    }
    return render(request, 'main/form_responses.html', context)


def create_form(request):
    if request.method == 'POST':
        form_form = FormCreateForm(request.POST)
        formset = QuestionFormSet(request.POST)

        if form_form.is_valid() and formset.is_valid():
            form_instance = form_form.save()
            questions = formset.save(commit=False)
            for question in questions:
                question.form = form_instance
                question.save()
            return redirect('form_list') 
    else:
        form_form = FormCreateForm()
        formset = QuestionFormSet()

    return render(request, 'main/create_form.html', {
        'form_form': form_form,
        'formset': formset
    })

def admin_home(request):
    forms = Form.objects.all()
    return render(request, 'main/admin_home.html', {'forms': forms})


def verify_user_id(request, form_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if Register.objects.filter(user_id=user_id).exists():
            request.session['user_id'] = user_id
            return redirect('form_detail', form_id=form_id)
        else:
            return redirect('register')  # لو مكانش يروح لصفحة التسجيل
    return render(request, 'main/verify_id.html', {'form_id': form_id})