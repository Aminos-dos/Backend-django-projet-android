from django.db import models
from django.db.models.deletion import CASCADE
from user.models import User
class Request(models.Model):
    sender = models.ForeignKey(User,on_delete=CASCADE,related_name="sender")
    receiver = models.ForeignKey(User,on_delete=CASCADE,related_name="receiver")
    added_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('sender', 'receiver',)