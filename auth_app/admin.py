from django.contrib import admin
from .models import User, Education, Language

# Register your models here.
admin.site.register(User)
admin.site.register(Education)
admin.site.register(Language)
