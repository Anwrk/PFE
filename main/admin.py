from django.contrib import admin
from .models import Register, Event
from .models import Form, Question, Response, Answer

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'phone_num', 'education_level','user_id')
    search_fields = ('name', 'email', 'phone_num')
    ordering = ('name',)

admin.site.register(Register, RegisterAdmin)
admin.site.register(Event)

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Answer)

admin.site.site_header = "جمعية القوافل العلمية"
admin.site.site_title = "جمعية القوافل العلمية"
admin.site.index_title = "لوحة التحكم"


