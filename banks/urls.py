from django.urls import path
from banks import views

urlpatterns=[
    path('',views.bank_index)

]