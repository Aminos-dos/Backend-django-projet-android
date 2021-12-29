from django.db import models

class User(models.Model):
    def get_profile_image(self,filename):
        return f'images/{self.username}/{"profile_image.png"}'
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100,default='salut ! j''utilise HolaApp')
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=get_profile_image,default='default.jpg')
    phone = models.CharField(max_length=12)
    gender = models.CharField(max_length=5,choices=[('M','Men'),('F','Female')],default='M')
    email = models.EmailField(max_length=100,unique=True)