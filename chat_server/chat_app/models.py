from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Userinfo(models.Model):
    nickName = models.CharField(null=True, blank=True, max_length=200)
    headImg = models.ImageField(upload_to="portrait/", null=True, blank=True)
    belong = models.OneToOneField(User,
                                  on_delete=models.CASCADE,
                                  related_name='userinfo_user',
                                  null=True,
                                  blank=True)

    def __int__(self):
        return self.id
