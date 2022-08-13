from django.shortcuts import redirect, render ,get_object_or_404
from .models import *
from home.models import *
from .filters import *

def blog(request):
    blog = Blog.objects.all()
    return render(request,"blog/blog.html",{'blog':blog})

def detail(request,id):
    blog = get_object_or_404(Blog,id = id)
    blog_all = Blog.objects.all()
    filter = BlogFilter(request.GET,queryset=blog_all)
    blog_all = filter.qs
    create = Blog.objects.all().order_by('-create')[:5]
    bazdid = sorted(blog_all,key= lambda t: t.total_asli(),reverse=True)
    tag = Blog.tags.all()
    similar = blog.tags.similar_objects()
    if request.user.is_authenticated:
        blog.views.add(request.user)
    else :
        blog.total += 1
        blog.save()
    views = blog.total_asli()
    return render(request,"blog/detail.html",{'blog':blog,'views':views,'filter':filter,'blog_all':blog_all,'create':create,'bazdid':bazdid,'similar':similar,'tag':tag})

def dastebandi(request,id):
    tag =  Blog.tags.get(id =id)
    blog = Blog.objects.filter(tags =tag)
    
    return render(request,'blog/dastebandi.html',{'tag':tag,'blog':blog})