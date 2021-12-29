from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('listMessages/<int:src>/<int:dest>',views.getAllMessage,name='list_messages'),
    path('<str:room_name>/<int:srcId>/<int:destId>', views.room, name='room'),
    path('seenMessage/<int:id>',views.seenMessage,name='seen_message'),
    path('listConvertation/<int:id>',views.getMyConvertation,name='list_convertation'),
    
]