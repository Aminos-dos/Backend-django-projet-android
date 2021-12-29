from django.urls import path
from .views import *

urlpatterns = [
    path('add',signup,name='register'),
    path('login',signin,name='login'),
    path('all',getAllUsers,name='get_all'),
    path('search/<str:name>',getAllUsers,name='get_all'),
    path('update/<int:id>',updateUser,name='update_user'),
    path('delete/<int:id>',deleteUser,name='delete_user'),
    path('resetPassword',resetPassword,name='reset_password'),
    path('users/<int:id>',getUsers,name='get_users')
]