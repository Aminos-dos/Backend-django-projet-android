from django.db import models
from django.db.models.deletion import CASCADE
from user.models import User
class Friend(models.Model):
    friend1 = models.ForeignKey(User,on_delete=CASCADE,related_name="friend1")
    friend2 = models.ForeignKey(User,on_delete=CASCADE,related_name="friend2")
    added_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('friend1', 'friend2',)