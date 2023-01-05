from django.urls import path 
from . import views

app_name= "accounts"
urlpatterns = [

    path("",views.accounts.as_view(),name="accounts"),
    path("register/",views.user_register,name="register"),
    path("login/",views.user_login ,name="login"),
    path("logout/",views.user_logout,name="logout" ),
    path("profile/",views.user_profile,name="profile"),
    path("update/",views.user_update,name = "update"),
    path("change_password/",views.user_change_password,name= "change_password"),
    path("login_phone/",views.user_login_phone,name="login_phone"),
    path("verify/",views.verify,name= "verify"),
    path("active/<uidb64>/<token>/",views.RegisterEmial.as_view(),name='active'),
    path("reset/",views.ResetPassword.as_view(),name='reset'),
    path("reset/done/",views.DonePassword.as_view(),name='reset_done'),
    path("confirm/<uidb64>/<token>/",views.ConfirmPassword.as_view(),name='password_reset_confirm'),
    path("confirm/done/",views.Complete.as_view(),name='complete'),
    path('favourite/',views.favourite,name='favourite'),
    path('history/',views.history,name='history'),
    path('view/',views.product_view,name='product_view'),
    

]
