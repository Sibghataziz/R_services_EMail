from django.urls import path
from .views import formView,pdfView

urlpatterns = [
    path('sendMail/', formView , name="form"),
    path('sendPdf/', pdfView , name="pdf")
]
