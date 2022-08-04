
from django.shortcuts import redirect, render,reverse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from random import randint
import ghasedakpack
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes ,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from order.models import *
from cart.models import *

class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

email_generator = EmailToken()

def accounts(requests):
    return render(requests, "accounts/accounts.html")

def user_register(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        form= UserregisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'], email=data['email'],first_name=data['first_name'],
                                    last_name=data['last_name'],password=data['password_2'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id)) 
            url  = reverse('accounts:active',kwargs ={'uidb64':uidb64,'token':email_generator.make_token(user)})
            link = 'http://'+domain+ url
            email = EmailMessage(
                'active user',
                link,
                'test<pouriael2002@gmail.com>',
                [data["email"]]
            )
            email.send(fail_silently=False)
            messages.warning(request,"please wait for activate ...",'warning')
            messages.success(request,"register is completed","success")
            return redirect("home:home")
        else:
            messages.success(request,"your are not registered","danger")
    else:
        form = UserregisterForm()
    context = {"form":form,'category':category,'compare':compare} 
    return render(request,'accounts/register.html',context)

def user_login(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        
    category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        form = UserloginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            remember = data['remember']
            try:
                user = authenticate(request,username =User.objects.get(email=data["user"]), password = data['password'])
            except:
                user = authenticate(request,username=data['user'], password = data['password'])
            if user is not None:
                login(request,user)
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(172800)
                messages.success(request,"welcome to my website",'success')
                return redirect("home:home")
            else:
                messages.error(request,"your login has error","danger")
    else:
        form = UserloginForm()
    context = {"form":form,'category':category,'compare':compare}
    return render(request,"accounts/login.html",context )

def user_logout(request):
    logout(request)
    messages.success(request,"success logout","success")
    return redirect("home:home")

class RegisterEmial(View):
    def get(self,request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
        return redirect('accounts:login')

@login_required(login_url="accounts:login")
def user_profile(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    Profile = formprofile.objects.get(user_id = request.user.id)
    return render(request,"accounts/profile.html",{"Profile":Profile,"category":category,'compare':compare})


@login_required(login_url="accounts:login")
def user_update(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        user_form = User_updateform(request.POST,instance=request.user)
        profile_form = Profile_updateform(request.POST,request.FILES,instance=request.user.formprofile)
        if profile_form and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"update completed","success")
            return redirect("accounts:profile")
    else:
        user_form = User_updateform(instance=request.user)
        profile_form = Profile_updateform(instance = request.user.formprofile)
    context = {"user_form":user_form,"profile_form":profile_form,'category':category,'compare':compare}
    return render (request,"accounts/update.html",context)


def user_change_password(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        
    category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,"password changed","success")
        else:
            messages.error(request,"password is not changed","danger")
    else:
        form  = PasswordChangeForm(request.user)
    context = {"form":form,'categroy':category,'compare':compare}
    return render(request,"accounts/change.html",context)

# bayad baraye estefade az service ersal payamak az ghasedak bekharim

def user_login_phone(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    global random_code,phone
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            phone =data["phone"]
            random_code = randint(100,1000)
            sms = ghasedakpack.Ghasedak("Your APIKEY")
            sms.send({'message':random_code, 'receptor' : phone, 'linenumber': '3000xxxxx' })
            return redirect("accounts:verify")
    else:
        form = PhoneForm()
    context = {"form":form,"category":category,'compare':compare} 
    return render(request,"accounts/login_phone.html",context)


def verify(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            data =form.cleaned_data
            if random_code == data["code"]:
                profile = formprofile.objects.get(phone = phone)
                user = User.objects.get(profile_id = profile.id)
                login(request,user)
                messages.success(request,f"welcome {user}","success")
            else:
                messages.error(request,"your code is wrong",'danger')
    else:
        form = CodeForm()
    return render(request,"accounts/code.html",{"form":form,"category":category,"compare":compare})

def favourite(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    product = request.user.fa_user.all()
    return render(request,'accounts/favourite.html',{'product':product,'category':category,'compare':compare})

def history(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    data = ItemOrder.objects.filter(user_id = request.user.id)
    return render(request,'accounts/history.html',{'data':data,'category':category,'compare':compare})

def product_view(request):
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    category = Category.objects.filter(sub_cat = False)
    product = Product.objects.filter(view = request.user.id)
    return render(request,'accounts/view.html',{'product':product,'category':category,'compare':compare})
    
class ResetPassword(auth_views.PasswordResetView):
    template_name = "accounts/reset.html"
    success_url = reverse_lazy("accounts:reset_done")
    email_template_name = "accounts/link.html"

class DonePassword(auth_views.PasswordResetDoneView):
    template_name = "accounts/done.html"

class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = "accounts/confirm.html"
    success_url = reverse_lazy("accounts:complete")

class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'
