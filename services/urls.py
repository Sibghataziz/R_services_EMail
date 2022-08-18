from django.urls import path
from .views import formView

urlpatterns = [
    path('sendMail/', formView , name="form"),
]
