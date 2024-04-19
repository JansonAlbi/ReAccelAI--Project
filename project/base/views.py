from django.shortcuts import redirect, render
from .models import User_info
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
import uuid

# Create your views here.
def home(request):
    return render(request,"landing_page/index.html")

def optimiz(request):
    return render(request,"optimization/optimiz.html")

def authView(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'signup':
            name = request.POST.get('sign_name')
            email = request.POST.get('sign_email')
            password = request.POST.get('sign_pass')
            confirm_password = request.POST.get('sign_conf_pass')
            phone_no=request.POST.get('signup_phone_number')

            if password == confirm_password:
                hashed_password = make_password(password)
                reaccelai_id = str(uuid.uuid4())
                while User_info.objects.filter(reaccelai_id=reaccelai_id).exists():
                    reaccelai_id = str(uuid.uuid4())
                new_user = User_info(reaccelai_id=reaccelai_id,name=name, email=email,password=hashed_password,phone_number=phone_no)
                new_user.save()
                return HttpResponse('Signup successful!')
            else:
                return HttpResponse('Passwords do not match. Please try again.')
        elif form_type == 'login':
            email = request.POST.get('login_email')
            password = request.POST.get('login_pass')
            try:
                user = User_info.objects.get(email=email)
                # Check if the provided password matches the hashed password
                if check_password(password, user.password):
                    request.session['user_id'] = str(user.reaccelai_id)
                    #return redirect('home')  # Redirect to home page after successful login
                    #return HttpResponse('Login successful!')
                    return render(request,"dashboard/dashboard.html")
                else:
                    error_message = "Invalid email or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except User_info.DoesNotExist:
                error_message = "User with this email does not exist."
                return render(request, 'login.html', {'error_message': error_message})
    else:
        
        return render(request, "registration/login.html")


