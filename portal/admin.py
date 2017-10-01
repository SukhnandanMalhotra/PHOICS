from django.contrib import admin
from .models import Document, Profile
# Register your models here.
admin.site.register(Document)   #brings your model in your admin
admin.site.register(Profile)