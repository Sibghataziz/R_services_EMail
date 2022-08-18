from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile
from .form import Register_form,Profile_form
from django.contrib.auth.models import User

# Create your views here.
local="127.0.0.1:8000"

def register_view(request):
    if request.method == "POST":
        Rform=Register_form(request.POST)
        Pform=Profile_form(request.POST,request.FILES)
        if Rform.is_valid() and Pform.is_valid():
            user = Rform.save()
            profile = Pform.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,"User created.")
            return redirect("login")
        else:
            messages.error(request,"Invalid Credentials.")
            return redirect("register")
    else:
        Rform=Register_form()
        Pform=Profile_form()
        context={"pform":Pform,"rform":Rform}
        return render(request,'accounts/register.html',context)

def home_view(request):
    if request.user.is_authenticated:
        user_name=request.user.username
        robj=User.objects.get(username=user_name)
        pobj=Profile.objects.get(user=robj.id)
        # print(obj)
        return render(request,"accounts/home.html",{"user":robj,"user1":pobj})
    else:
        messages.error(request,"You have been Logout.")
        return redirect('login')

