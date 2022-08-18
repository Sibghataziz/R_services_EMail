from django.shortcuts import render,redirect

def homeView(request):
    if request.user.is_authenticated:
       return redirect("form")
    return render(request,"home.html")