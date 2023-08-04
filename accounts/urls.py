from django.urls import path
from accounts import views

urlpatterns=[
    path('',views.account_index),
    path('register',views.register_user),
    path('login',views.login_user),
    path('logout',views.logout_user),
    path('profile/view',views.view_login_user,name='profile')
,
]