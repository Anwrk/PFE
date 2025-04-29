from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.index , name="main"),
    path("register/", views.register, name="register"),
    path("events/", views.events, name="events"),
    path("events/<slug:slug>/", views.event_detail, name="event_details"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
