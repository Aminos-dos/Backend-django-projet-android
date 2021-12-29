from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestModel(admin.ModelAdmin):
    list_filter = ('id','sender','receiver','added_date')
    list_display = ('id','sender','receiver','added_date')