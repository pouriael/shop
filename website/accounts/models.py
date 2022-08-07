
from home.models import *
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phone_field import PhoneField
from django_jalali.db import models as jmodels


class formprofile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,verbose_name = 'کاربر',related_name='userp')
    phone = PhoneField(null=True,blank=True,verbose_name = 'شماره همراه')
    address = models.CharField(max_length=50,null=True,blank=True,verbose_name = 'آدرس')
    profile_image = models.ImageField(upload_to = 'profile/',default="",null =True,blank=True,verbose_name = 'عکس پروفایل')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها '

    def __str__(self) :
        return self.user.username

   

def profile_signals(sender,**kwargs):
    if kwargs["created"]:
        profile_user = formprofile(user = kwargs["instance"])
        profile_user.save() 

post_save.connect(profile_signals,sender= User)


