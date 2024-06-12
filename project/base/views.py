import os
from django.core.files.storage import default_storage
from .models import UploadedFile
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

from django.core.mail import send_mail, BadHeaderError
import json
import smtplib  # Importing SMTPException for handling email sending errors

from django.shortcuts import render, get_object_or_404

from .models import login_at

import logging

logger = logging.getLogger(__name__)

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
                    user_id = request.session.get('user_id', 'default_value')
                    loginat=login_at(email=email,user_name=user.name,reaccel_id=user_id)
                    loginat.save()
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
    """if request.method == 'POST':
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
    else:"""
    
    return render(request, 'dashboard/ModelCreationLanding.html')


def widgets(request):
    return render(request, 'dashboard/widgets.html')




def tables(request):
    return render(request, "dashboard/tables.html")




def grid(request):
    return render(request, "dashboard/grid.html")




def History(request):
    data = login_at.objects.values('email','user_name', 'login_at')
    return render(request, "dashboard/History.html", {'data': data})




def project_history(request):
    user_id = request.session.get('user_id', 'default_value')
    data = UploadedFile.objects.filter(reaccel_id=user_id).values('project_name','class_names', 'file','timestamp','epoch_value','batch_size','learning_rate','project_status','model_type')
    return render(request, "dashboard/project_history.html", {'data': data})




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
    """print('creationModel project Details: ')
    if request.method == 'POST':
        print('details about project name and modeltype')
        form_type = request.POST.get('form_type')
        if form_type == 'modellanding':
            global project_name
            global model_type
            global user_id
            user_id = request.session.get('user_id','default_value')
            project_name = request.POST.get('project_name')
            model_type = request.POST.get('model_type')
            
        if form_type == 'uploading':
            class_list=request.POST.get('class_list')
            file_list=request.POST.get('file_list')
            epoch_value=request.POST.get('epoch')
            batch_size=request.POST.get('batchsize')
            learning_rate=request.POST.get('learningrate')
            prj_status=1
            i=1
            class_list = int(class_list)
            file_list = int(file_list)
            arrayclass=[]
            classnames=[]
            filenames=[]
            uploadedfiles=[]
            file_path=[]
            print("project name="+ project_name)
            print(f"model type={model_type}")
            print("user-is="+user_id)
            while i <= class_list:
                hey="class"+ str(i) 
                arrayclass.append(hey)
                i=i+1
            i=1
            while i <= class_list:
                classname=request.POST.get('class'+str(i))
                classnames.append(classname)
                i=i+1
            for classname in arrayclass:
                print(classname)
            for classname in classnames:
                print(classname)
            print("epoch="+epoch_value)
            print("batch-size="+batch_size)
            print("learning-rate="+learning_rate)
            i=1
            while i <= file_list:
                namefile='file'+str(i)
                filenam=request.FILES(namefile)
                filenames.append(filenam)
                i=i+1
            i=1
            while i <= class_list:
                file_nam=filenames[i]
                filepath=os.path.join(project_name, classnames[i], file_nam.name)
                file_path.append(filepath)
            i=1
            while i <= file_list:
                default_storage.save(file_path[i],filenames[i])
            i=1
            while i <= file_list and i <= class_list:
                UploadedFile.objects.create(reaccel_id=user_id,project_name=project_name,class_names=classnames[i],file=file_path[i],epoch_value=epoch_value,batch_size=batch_size,learning_rate=learning_rate,project_status=prj_status)
    """
    print('creationModel project Details: ')
    if request.method == 'POST':
        print('details about project name and modeltype')
        form_type = request.POST.get('form_type')
        if form_type == 'modellanding':
            global project_name
            global model_type
            global user_id
            user_id = request.session.get('user_id', 'default_value')
            project_name = request.POST.get('project_name')
            model_type = request.POST.get('model_type')
            
        if form_type == 'uploading':
            class_list = int(request.POST.get('class_list'))
            file_list = int(request.POST.get('file_list'))
            epoch_value = int(request.POST.get('epoch'))
            batch_size = int(request.POST.get('batchsize'))
            learning_rate = float(request.POST.get('learningrate'))
            prj_status = 1

            classnames = []
            file_paths = []
            uploaded_files = []
            
            print(f"project name = {project_name}")
            print(f"model type = {model_type}")
            print(f"user-id = {user_id}")
            
            for i in range(1, class_list + 1):
                classname = request.POST.get('class' + str(i))
                if classname:
                    classnames.append(classname)

            for classname in classnames:
                print(classname)
                
            print(f"epoch = {epoch_value}")
            print(f"batch-size = {batch_size}")
            print(f"learning-rate = {learning_rate}")
            
            for i in range(1, file_list + 1):
                file = request.FILES.get('file' + str(i))
                if file:
                    filepath = os.path.join(project_name, classnames[i-1], file.name)
                    file_paths.append(filepath)
                    uploaded_files.append(file)
                    
            for i, filepath in enumerate(file_paths):
                default_storage.save(filepath, uploaded_files[i])
            
            for i, filepath in enumerate(file_paths):
                UploadedFile.objects.create(
                    reaccel_id=user_id,
                    project_name=project_name,
                    class_names=classnames[i],
                    file=filepath,
                    epoch_value=epoch_value,
                    batch_size=batch_size,
                    learning_rate=learning_rate,
                    project_status=prj_status,
                    model_type=model_type
                )
    return render(request, "dashboard/ModelCreation.html")

def send_otp(email):
    otp_instance = OTP.objects.create(email=email)
    otp_instance.generate_otp()
    otp_instance.save()
    
    try:
        sent_status=send_mail(
            'ReaccelAi OTP Code',
            f'ReaccelAi Your OTP code is {otp_instance.otp}',
            'pinniboinarajesh640@gmail.com',
            [email],
            fail_silently=False,
        )
    except BadHeaderError:
        #return JsonResponse({'success': False, 'message': 'Invalid header found.'})
        return 0
    except smtplib.SMTPRecipientsRefused:
        #return JsonResponse({'success': False, 'message': 'Recipient address refused. Invalid email address.'})
        return 0
    except smtplib.SMTPException as e:
        #return JsonResponse({'success': False, 'message': f'SMTP error occurred: {str(e)}'})
        return 0
    except Exception as e:
        #return JsonResponse({'success': False, 'message': str(e)})
        return 0
    
    print(f'otp code:{otp_instance.otp}')
    return sent_status

def send_otp_ajax(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            sent_status=send_otp(email)
            print("otp sent")
            print(sent_status)
            if sent_status == 1:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False})

def verify_otp_ajax(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        email = data.get('email')
        otp_1 = data.get('otp_1')
        otp_2 = data.get('otp_2')
        otp_3 = data.get('otp_3')
        otp_4 = data.get('otp_4')
        otp = f"{otp_1}{otp_2}{otp_3}{otp_4}"
        print(f"entered otp is :{otp}")
        otp_instance = OTP.objects.filter(email=email, otp=otp).first()
        
        if otp_instance and otp_instance.timestamp > timezone.now() - timedelta(minutes=5):
            # Here you can handle the signup logic
            verification_success(email)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    
    
def verification_success(email):
    
    send_mail(
            'ReaccelAi Verification Sucessfull',
            'Lets Enjoy Features of ReaccelAi WebApplication',
            'pinniboinarajesh640@gmail.com',
            [email],
            fail_silently=False,
        )
    


def user_profile(request):
    """user_id = request.session.get('user_id', 'default_value')
    data = User_info.objects.filter(reaccelai_id=user_id).values('name','created_at', 'email','phone_number')
    context = {
        'user': data,
    }"""
    user_id = request.session.get('user_id', 'default_value')
    user = get_object_or_404(User_info, reaccelai_id=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'dashboard/profile.html', context)
    #eturn render(request, 'dashboard/profile.html', {'data': data})
    