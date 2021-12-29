from django.contrib import admin
from .models import User

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_filter = ('id','name','username','description','password','photo','phone','gender','email')
    list_display = ('id','name','username','password','photo','phone','gender','email')