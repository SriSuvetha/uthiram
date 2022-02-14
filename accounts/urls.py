from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.login_user, name='home'),
    path('login', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup', views.signup_user, name='signup'),
    path('register/<token>', views.register, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('change_password/<token>', views.change_password, name='change_password'),
    path('donor_register', views.donor_register, name='donor_register'),
    path('donor_edit', views.donor_edit, name='donor_edit'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('requestpage/', views.requestpage),
    path('loginpage/', views.loginpage),
    path('signuppage/', views.signuppage),
    path('userreq/', views.userreq),
    path('yourdonationspage/', views.yourdonationspage),
    path('yourrequestspage/', views.yourrequestspage),
    path('donoreditpage/', views.donoreditpage),
    path('', include('request.urls')),

]
