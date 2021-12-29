from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('user.urls')),
    path('api/request/',include('request.urls')),
    path('api/message/',include('message.urls')),
    path('api/friend/',include('friend.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
