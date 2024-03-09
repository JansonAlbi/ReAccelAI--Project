from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"landing_page/index.html")
def authView(request):

    if request.method == "POST":
        username = request.POST['uname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        phoneno = request.POST['phone-number']

        user1 = User.objects.create_user(username, email, pass1)
        user1.phone_number = phoneno
        user1.save()

        #return redirect('login')

        messages.success(request,"Your Account Has Been Successfully Created")
    return render(request, "registration/login.html")
