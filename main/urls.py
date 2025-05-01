from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.index , name="main"),
    path("register/", views.register, name="register"),
    path("events/", views.events, name="events"),
    path("events/<slug:slug>/", views.event_detail, name="event_details"),
    path('forms', views.form_list, name='form_list'),
    path('create-form/', views.create_form, name='create_form'),
    path('form/<int:form_id>/', views.form_detail, name='form_detail'),
    path('form/<int:form_id>/responses/', views.form_responses, name='form_responses'),
    path('frm', views.answers_list, name='answers_list'),
    path('admin-view/', views.admin_home, name='admin_home'),
    path('form/<int:form_id>/verify/', views.verify_user_id, name='verify_user_id'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
