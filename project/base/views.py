from django.shortcuts import redirect, render
from .models import User_info,Login_history
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
import uuid
from django.shortcuts import render, redirect

from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.auth import authenticate, login

from django.core.mail import send_mail
from .models import OTP
from django.utils import timezone
from datetime import timedelta
import json
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request,"landing_page/index.html")

def optimiz(request):
    #if request.method == 'POST':
     #   files = request.FILES.getlist('file')
    #    for file in files:
    #        uploaded_file = UploadedFile(file=request.FILES['file'])
     #       uploaded_file.save()
 #   else:
      #  return HttpResponse('file_upload failed')
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
                #return HttpResponse('Signup successful!')
                #return render(request, "registration/signupSuccessful.html")
                messages.success(request, 'Signup successful!')
                return render(request, 'registration/login.html', {'form': User_info()})
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
                    """if user is not None:
                        # Log the user in
                        login_hist=Login_history(user_info=email)  # Store login history
                        login_hist.save()"""
                    #return redirect('home')  # Redirect to home page after successful login
                    #return HttpResponse('Login successful!')
                    #return render(request,"dashboard/dashboard.html")
                    return index(request)
                else:
                    error_message = "Invalid email or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except User_info.DoesNotExist:
                error_message = "User with this email does not exist."
                return render(request, 'login.html', {'error_message': error_message})
    else:
        
        return render(request, "registration/login.html")


from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')


def ModelCreation(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files[]')  # Retrieve list of uploaded files
        if uploaded_files:
            s3 = S3Boto3Storage()
            for uploaded_file in uploaded_files:
                try:
                    filename = uploaded_file.name
                    s3.save(filename, uploaded_file)
                    # Process each uploaded file as needed
                except Exception as e:
                    # Handle errors if file upload fails
                    return HttpResponse("Error uploading file")
            return HttpResponse("All files uploaded successfully!")
        else:
            return HttpResponse("No files selected for upload.")
    else:
        return render(request, 'dashboard/ModelCreationLanding.html')


def widgets(request):
    return render(request, 'dashboard/widgets.html')




def tables(request):
    return render(request, "dashboard/tables.html")




def grid(request):
    return render(request, "dashboard/grid.html")




def History(request):
    data = User_info.objects.values('name', 'created_at')
    return render(request, "dashboard/History.html", {'data': data})




def form_wizard(request):
    return render(request, "dashboard/form_wizard.html")




def buttons(request):
    return render(request, "dashboard/buttons.html")




def icon_material(request):
    return render(request, "dashboard/icon-material.html")




def icon_fontawesome(request):
    return render(request, "dashboard/icon-fontawesome.html")




def elements(request):
    return render(request, "dashboard/elements.html")




def gallery(request):
    return render(request, "dashboard/gallery.html")





def invoice(request):
    return render(request, "dashboard/invoice.html")



def chat(request):
    return render(request, "dashboard/chat.html")

def Creation(request):
    return render(request, "dashboard/ModelCreation.html")

def send_otp(email):
    otp_instance = OTP.objects.create(email=email)
    otp_instance.generate_otp()
    otp_instance.save()
    
    send_mail(
        'ReaccelAi OTP Code',
        f'ReaccelAi Your OTP code is {otp_instance.otp}',
        'pinniboinarajesh640@gmail.com',
        [email],
        fail_silently=False,
    )
    print(f'otp code:{otp_instance.otp}')

def send_otp_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            send_otp(email)
            print("otp sent")
            #return JsonResponse({'success': True})
    return JsonResponse({'success': False})