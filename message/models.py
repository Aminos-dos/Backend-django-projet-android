from django.db import models
from user.models import User
class Message(models.Model):
    userSrc = models.ForeignKey(User,related_name='user_src',on_delete=models.CASCADE)
    userDst = models.ForeignKey(User,related_name='user_dest',on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    seen = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)