from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessagetModel(admin.ModelAdmin):
    list_filter = ('id','userSrc','userDst','content','seen','added_date')
    list_display = ('id','userSrc','userDst','content','seen','added_date')