from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"landing_page/index.html")
def authView(request):
    return render(request, "registration/login.html")
