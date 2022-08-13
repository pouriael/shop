from random import choices
from tkinter import Widget
import django_filters
from django import forms
from .models import *

class BlogFilter(django_filters.FilterSet):
    choice_2 ={
        ('قدیمی ترین','قدیمی ترین'),
        ('جدید ترین','جدید ترین'),
        
    }

    create = django_filters.ChoiceFilter(choices = choice_2,method = 'create_filter')


    def create_filter(self,queryset,name,value):
        data = "create" if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)


  

