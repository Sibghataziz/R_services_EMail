from pickle import FALSE
import re
from time import strftime
from venv import create
from django.shortcuts import render, redirect
from .form import NameForm, PdfForm
from django.contrib import messages
from accounts.models import Profile
from django.contrib.auth.models import User
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders

import random
import smtplib
import datetime
import pdfkit
import os


# Create your views here.
def formView(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        content = request.POST.get("Content")
        emails = request.POST.get('Emails')
        Your_Email = request.POST.get("Your_Email")
        subject = request.POST.get("Subject")
        password = request.POST.get('Your_Two_Factor_Password')
        username = request.POST.get("Username")
        emails = emails.split("\r\n")
        user_name = request.user.username

        robj = User.objects.get(username=user_name)
        pobj = Profile.objects.get(user=robj.id)
        success = False
        if(pobj.numberOfMails<10000):
            success = sendEmail(request, content, emails, Your_Email, password, username,subject)
        else:
            messages.error(request,"Email limit exceeded.")
        # print(success)
        if success:
            pobj.numberOfMails += len(emails)
            pobj.save()

    user_name = request.user.username
    robj = User.objects.get(username=user_name)
    pobj = Profile.objects.get(user=robj.id)
    context = {
    "form": NameForm,
    "count": pobj.numberOfMails
    }
    return render(request, "services/form.html", context)


def pdfView(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        content = request.POST.get("Content")
        emails = request.POST.get('Emails')
        Your_Email = request.POST.get("Your_Email")
        subject = request.POST.get("Subject")
        text = request.POST.get("TextBox")
        password = request.POST.get('Your_Two_Factor_Password')
        username = request.POST.get("Username")
        emails = emails.split("\r\n")
        user_name = request.user.username

        robj = User.objects.get(username=user_name)
        pobj = Profile.objects.get(user=robj.id)
        success = False
        if(pobj.numberOfMails<10000):
            success = sendPdf(request, content, emails, Your_Email, password, username,subject,text)
        else:
            messages.error(request,"Email limit exceeded.")
        # print(success)
        if success:
            pobj.numberOfMails += len(emails)
            pobj.save()

    user_name = request.user.username
    robj = User.objects.get(username=user_name)
    pobj = Profile.objects.get(user=robj.id)
    context = {
    "form": PdfForm,
    "count": pobj.numberOfMails
    }
    return render(request, "services/pdf.html", context)

def sendEmail(request, content, emails, Your_Email, password, username,subject):
    # popUp = ""
    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
            step=1
            server_check = server.ehlo()
            step=2
            TLS_check = server.starttls()
            step=3
            Login_check = server.login(Your_Email, password)
            step=4
            for email in emails:
                orderno, refno = createRandom()
                date = createDate()
                content = content.format(orderno=orderno, refno=refno,date = date)
                msg = MIMEMultipart('alternative')
                msg['From'] = formataddr((username,"Norton"))
                msg['To'] = email
                msg['Subject'] = subject
                body = MIMEText(content, "HTML")
                msg.attach(body)
                msgs = msg.as_string()
                server.sendmail(Your_Email, email, msgs)
            messages.success(request,"All emails sent")
            return True
    except:
        if step==1 or step==2:
            messages.error(request,"Gmail server is not responding")
            # return render(request, "services/error.html", {"msg": "Gmail server is not responding"})
        elif step==3:
            # print(1)
            messages.error(request,"Invalid Login Credentials")
            # return render(request, "services/error.html", {"msg": "Invalid Login Credentials"})
        else:
            messages.error(request,"Something went Wrong")
            # return render(request, "services/error.html", {"msg": "Something went Wrong"})
        return False

def sendPdf(request, content, emails, Your_Email, password, username,subject,text):
    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
            step=1
            server_check = server.ehlo()
            step=2
            TLS_check = server.starttls()
            step=3
            Login_check = server.login(Your_Email, password)
            step=4
            for email in emails:
                orderno, refno = createRandom()
                date = createDate()
                content = content.format(orderno=orderno, refno=refno,date = date)
                path = f"media\{refno}{orderno}.pdf"
                pdfkit.from_string(content,path)
                msg = MIMEMultipart('alternative')
                msg['From'] = formataddr((username,"Norton"))
                msg['To'] = email
                msg['Subject'] = subject
                body = MIMEText(text)
                msg.attach(body)
                attachment = open(os.path.abspath(path), 'rb')
                at_pdf = MIMEBase('application', 'octet-stream')
                at_pdf.set_payload((attachment).read())
                encoders.encode_base64(at_pdf)
                at_pdf.add_header('Content-Disposition', f"attachment; filename= Order_Receipt.pdf")
                msg.attach(at_pdf)
                msgs = msg.as_string()
                server.sendmail(Your_Email, email, msgs)
            messages.success(request,"All emails sent")
            return True
    except:
        if step==1 or step==2:
            messages.error(request,"Gmail server is not responding")
            # return render(request, "services/error.html", {"msg": "Gmail server is not responding"})
        elif step==3:
            # print(1)
            messages.error(request,"Invalid Login Credentials")
            # return render(request, "services/error.html", {"msg": "Invalid Login Credentials"})
        else:
            messages.error(request,"Something went Wrong")
            # return render(request, "services/error.html", {"msg": "Something went Wrong"})
        return False

def createRandom():
    orderno = random.randint(9000000000, 9999999999)
    a = random.randint(65, 90)
    b = random.randint(1, 9)
    c = random.randint(97, 122)
    d = random.randint(65, 90)
    e = random.randint(65, 90)
    f = random.randint(97, 122)
    g = random.randint(9526, 16852)
    refno = f"{chr(a)}{b}{chr(c)}{g}{chr(d)}{chr(e)}{chr(f)}"
    return orderno, refno

def createDate():
    date = datetime.datetime.now()
    return f"{date.strftime('%d')}-{date.strftime('%b')}-{date.strftime('%Y')}"

# def sendEmail(request, content, emails, Your_Email, password, username):
#     # # popUp = ""
#     # try:
#         with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
#             step=1
#             server_check = server.ehlo()
#             step=2
#             TLS_check = server.starttls()
#             step=3
#             Login_check = server.login(Your_Email, password)
#             step=4
#             for email in emails:
#                 orderno, refno = createRandom()
#                 date = createDate()
#                 content = content.format(orderno=orderno, refno=refno,date = date)
#                 msg = MIMEMultipart('alternative')
#                 msg['From'] = formataddr((username,"Norton"))
#                 msg['To'] = email
#                 msg['Subject'] = f"Thank you for your order-{orderno}"
#                 body = MIMEText(content, "HTML")
#                 msg.attach(body)
#                 msgs = msg.as_string()
#                 server.sendmail(Your_Email, email, msgs)
#             messages.success(request,"All emails sent")
#             return True
#     # except:
#     #     if step==1 or step==2:
#     #         messages.error(request,"Gmail server is not responding")
#     #         # return render(request, "services/error.html", {"msg": "Gmail server is not responding"})
#     #     elif step==3:
#     #         # print(1)
#     #         messages.error(request,"Invalid Login Credentials")
#     #         # return render(request, "services/error.html", {"msg": "Invalid Login Credentials"})
#     #     else:
#     #         messages.error(request,"Something went Wrong")
#     #         # return render(request, "services/error.html", {"msg": "Something went Wrong"})
#     #     return False