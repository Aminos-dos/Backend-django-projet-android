from django.contrib import admin
from .models import Friend


@admin.register(Friend)
class FriendModel(admin.ModelAdmin):
    list_filter = ('id','friend1','friend2','added_date')
    list_display = ('id','friend1','friend2','added_date')
