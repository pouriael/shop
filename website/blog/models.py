from distutils.command.upload import upload
from itertools import product
from operator import truediv
from tkinter.tix import Tree
from turtle import tracer
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField 
from taggit.managers import TaggableManager
from accounts.models import * 
from django.forms import BooleanField, ModelForm
from django.db.models import Avg
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Blog(models.Model):
    name = models.CharField(max_length=200,verbose_name='اسم')
    create = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog')
    tags =  TaggableManager(blank=True,verbose_name = 'نسبت تشابه')
    text = RichTextUploadingField(blank =True,null=True)
    kholase = models.CharField(max_length=500,default='Lorem Ipsum is simply dummy text of the printing and typesetting industry.')
    views = models.ManyToManyField(User,blank=True,related_name='views_blog')
    total_views = models.IntegerField(null=True,blank=True,default=0)
    total = models.IntegerField(default=0)


    def total_views(self):
        return self.views.count()

    def total_asli(self):
        data = self.total_views()+self.total
        return data

    def __str__(self):
        return self.name

