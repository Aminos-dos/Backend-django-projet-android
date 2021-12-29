from django.urls import path
from .views import *


urlpatterns = [
    path('deleteFriend/<int:id>',deleteFromFriend,name='delete_from_friend')
]