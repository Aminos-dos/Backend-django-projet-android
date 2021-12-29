from django.urls import path
from .views import *


urlpatterns = [
    path('sendRequest',sendRequest,name='send_request'),
    path('deleteRequest/<int:id>',deleteRequest,name='delete_request'),
    path('acceptRequest',acceptRequest,name='accept_request'),
]