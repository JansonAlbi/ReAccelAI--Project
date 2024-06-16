import os
from django.core.files.storage import default_storage
from .models import UploadedFile
from .models import admin_iam_users
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

from django.db.models.functions import TruncMonth
from django.db.models import Count

from django.core.serializers.json import DjangoJSONEncoder

import json
from django.http import JsonResponse

from django.core.mail import send_mail, BadHeaderError
import json
import smtplib  # Importing SMTPException for handling email sending errors

from django.shortcuts import render, get_object_or_404

from django.contrib.auth import update_session_auth_hash

from django.urls import reverse

from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout

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
            allpermissions=1
            if password == confirm_password:
                hashed_password = make_password(password)
                reaccelai_id = str(uuid.uuid4())
                while User_info.objects.filter(reaccelai_id=reaccelai_id).exists():
                    reaccelai_id = str(uuid.uuid4())
                new_user = User_info(reaccelai_id=reaccelai_id,name=name, email=email,password=hashed_password,phone_number=phone_no,allpermissions=allpermissions)
                new_user.save()
                #return HttpResponse('Signup successful!')
                #return render(request, "registration/signupSuccessful.html")
                messages.success(request, 'Signup successful!')
                return render(request, 'registration/login.html', {'form': User_info()})
            else:
                return HttpResponse('Passwords do not match. Please try again.')
        elif form_type == 'login':
            global whologged
            """email = request.POST.get('login_email')
            password = request.POST.get('login_pass')
            try:
                user = User_info.objects.get(email=email)
                #iamuser = admin_iam_users.objects.get(iam_user_name=email)
                iam = get_object_or_404(admin_iam_users, iam_user_name=email)
                # Check if the provided password matches the hashed password
                if check_password(password, user.password):
                    print("admin user")
                    request.session['user_id'] = str(user.reaccelai_id)
                  
                    #return redirect('home')  # Redirect to home page after successful login
                    #return HttpResponse('Login successful!')
                    #return render(request,"dashboard/dashboard.html")
                    user_id = request.session.get('user_id', 'default_value')
                    loginat=login_at(email=email,user_name=user.name,reaccel_id=user_id)
                    loginat.save()
                    return index(request)
                elif iam.iam_user_password == password:
                    print("iam user")
                    request.session['user_id'] = str(iam.reaccel_id)
                    if user_id:
                        # Fetch a single instance
                        user = get_object_or_404(admin_iam_users, iam_user_name=email)
                        context = {'user': user}
                        return index(request,context)
                    else:
                        context = {'error': 'No user_id provided'}
                else:
                    error_message = "Invalid email or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except User_info.DoesNotExist:
                error_message = "User with this email does not exist."
                #return render(request, 'login.html', {'error_message': error_message})
    else:
        
        return render(request, "registration/login.html")"""
            
            global iam
            email = request.POST.get('login_email')
            password = request.POST.get('login_pass')
            user = None

            try:
                # Check if user exists in User_info
                user = User_info.objects.get(email=email)
                if check_password(password, user.password):
                    # User exists and password matches
                    request.session['user_id'] = str(user.reaccelai_id)
                    loginat = login_at(email=email, user_name=user.name, reaccel_id=request.session['user_id'])
                    loginat.save()
                    #context = {'user': user}
                    whologged=1
                    return index(request)
                    #return index(request)
                else:
                    error_message = "Invalid email or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except User_info.DoesNotExist:
                pass  # Proceed to check in admin_iam_users

            try:
                # Check if user exists in admin_iam_users
                iam_user = admin_iam_users.objects.get(iam_user_name=email)
                if iam_user.iam_user_password == password:
                    # User exists and password matches
                    request.session['user_id'] = str(iam_user.reaccel_id)
                    iam=iam_user.iam_user_name
                    """context = {'user': iam_user}"""
                    whologged=2
                    return index(request)
                else:
                    error_message = "Invalid email or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except admin_iam_users.DoesNotExist:
                error_message = "User with this email does not exist."
                return render(request, 'login.html', {'error_message': error_message})

        else:
            # Handle unknown form_type
            return HttpResponse('Invalid form type.')
    
    else:
        return render(request, "registration/login.html")

    # Add a final return to ensure an HttpResponse is always returned
    return render(request, "registration/login.html", {'error': 'Invalid request method'})
            


from django.shortcuts import render

# Create your views here.
def index(request):
    """#user_logins = login_at.objects.all()
    user_id = request.session.get('user_id', 'default_value')
    #user_logins = login_at.objects.filter(reaccel_id=user_id).values('login_at')
    # Prepare data for the graph
    timestamps = [login.timestamp for login in user_logins]
    data = {
    'labels': [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps],
    'data': [1] * len(timestamps) # Using 1 to count each login
    }

    data_json = json.dumps(data, cls=DjangoJSONEncoder)
    context = {
    'data_json': data_json,
    }
    #return render(request, 'dashboard/dashboard.html', context)
    # Aggregate login data by month
    monthly_logins = (
    login_at.objects.filter(reaccel_id=user_id,).annotate(month=TruncMonth('login_at'))
    .values('month')
    .annotate(count=Count('id'))
    .order_by('month')
    )

    monthly_login_data = {log['month'].strftime('%Y-%m'): log['count'] for log in monthly_logins}

    # Prepare data for login chart
    data = {
    'labels': list(monthly_login_data.keys()),
    'data': list(monthly_login_data.values())
    }

    data_json = json.dumps(data, cls=DjangoJSONEncoder)
    context = {
    'data_json': data_json,
    }
    #return render(request, 'dashboard/dashboard.html', context)
    # Filter the login data for a specific user using reaccel_id
    user_logins = login_at.objects.filter(reaccel_id=user_id)
    
    # Aggregate login data by month
    monthly_logins = (
        user_logins.annotate(month=TruncMonth('login_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

     # Debug: Print the raw query results
    print("Monthly Logins Raw Data:", list(monthly_logins))

    monthly_login_data = {log['month'].strftime('%Y-%m'): log['count'] for log in monthly_logins}

    # Debug: Print the transformed data
    print("Monthly Login Data:", monthly_login_data)

    # Prepare data for login chart
    data = {
        'labels': list(monthly_login_data.keys()),
        'data': list(monthly_login_data.values())
    }

    data_json = json.dumps(data, cls=DjangoJSONEncoder)
    context = {
        'data_json': data_json,
    }"""
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, 'dashboard/index.html', context)


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
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}

    return render(request, 'dashboard/ModelCreationLanding.html', context)


def widgets(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, 'dashboard/widgets.html', context)




def tables(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/tables.html", context)




def grid(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/grid.html", context)




def History(request):
    context = {}
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    data = login_at.objects.values('email','user_name', 'login_at')
    context['data'] = data
    return render(request, "dashboard/History.html",context)




def project_history(request):
    context = {}
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    user_id = request.session.get('user_id', 'default_value')
    data = UploadedFile.objects.filter(reaccel_id=user_id).values('project_name','class_names', 'file','timestamp','epoch_value','batch_size','learning_rate','project_status','model_type')
    context['data'] = data
    return render(request, "dashboard/project_history.html",context)




def my_iam_users(request):
    context = {}
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    user_id = request.session.get('user_id', 'default_value')
    data = admin_iam_users.objects.filter(reaccel_id=user_id).values('iam_user_name','iam_user_password', 'access_permissions','user_createdon','description')
    context['data'] = data
    return render(request, "dashboard/iam.html",context)




def icon_material(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/icon-material.html", context)




def icon_fontawesome(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/icon-fontawesome.html", context)




def elements(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/elements.html", context)




def gallery(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/gallery.html", context)





def invoice(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/invoice.html", context)



def chat(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/chat.html", context)

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
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, "dashboard/ModelCreation.html", context)

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


def verify_otp_newpassword(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
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
    context = {}
    user_id = request.session.get('user_id', 'default_value')
    user = get_object_or_404(User_info, reaccelai_id=user_id)
    
    """profilecontext = {
        'profileuser': user,
    }"""
    context['profileuser']=user
    
    
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    return render(request, 'dashboard/profile.html',context)
    #eturn render(request, 'dashboard/profile.html', {'data': data})
    

def profile_settings(request):
    user_id = request.session.get('user_id', 'default_value')
    user = get_object_or_404(User_info, reaccelai_id=user_id)
    print('profile settings out')
    context = {}
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'profilesettings':
            print('profile settings in')
            # Get the new data from the form
            new_name = request.POST.get('first_name')
            new_phone_number = request.POST.get('phone_number')
        
            # Update the user object
            user.name = new_name
            user.phone_number = new_phone_number
            user.save()
        
            # Add a success message
            #messages.success(request, 'Your profile has been updated successfully!')
        
            # Redirect to the same page to show the updated info
            #return redirect('user_profile')
            """profilesettingscontext = {
            'profilesettingsuser': user,
            }"""
            context['profilesettingsuser']=user
            if whologged == 1:
                user_id = request.session.get('user_id', 'default_value')
                user = User_info.objects.get(reaccelai_id=user_id)
                context['user'] = user
            if whologged == 2:
                iamuser = admin_iam_users.objects.get(iam_user_name=iam)
                context['user'] = iamuser
            return render(request, 'dashboard/profilesettings.html',context)

    """profilesettingscontext = {
        'profilesettingsuser': user,
    }"""
    context['profilesettingsuser']=user
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    return render(request, 'dashboard/profilesettings.html',context)
    #eturn render(request, 'dashboard/profile.html', {'data': data})
    

def update_password_send_otp_ajax(request):
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

def updating_password_profile_settings(request):
    user_id = request.session.get('user_id', 'default_value')
    user = get_object_or_404(User_info, reaccelai_id=user_id)
    print('profile settings out')
    context = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        new_password=data.get('new_password')
        confirm_password=data.get('confirm_password')
        updating_newpassword = data.get('updating_newpassword')
        if updating_newpassword == 1:
            #new_password = request.POST.get('newpassword')
            #confirm_password = request.POST.get('confirm_password')
            print("updating new password in DB")
            # Update password if provided and they match
            if new_password and new_password == confirm_password:
                user = User_info.objects.get(email=email)
                user.password = make_password(new_password)  # Hash the new password
                user.save()
                return JsonResponse({'success': True})
            elif new_password and new_password != confirm_password:
                return JsonResponse({'success': False})
    
    """profilesettingscontext = {
        'profilesettingsuser': user,
    }"""
    context['profilesettingsuser']=user
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    return render(request, 'dashboard/profilesettings.html',context)


def logout_view(request):
    auth_logout(request)
    #return render(request, "registration/login.html")
    return authView(request)



def aboutus(request):
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, 'dashboard/about.html',context)

def helpme(request):
    print("help.............")
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}
    return render(request, 'dashboard/help.html',context)

def helpme_send_query(request):
    if request.method == 'POST':
        print('help out')
        data = json.loads(request.body)
        form_type = data.get('form_type')
        ticket_raised = data.get('ticket_raised')
        if form_type == 'help':
            print('help in')
            user_id = request.session.get('user_id', 'default_value')
            data = User_info.objects.filter(reaccel_id=user_id).values('email')
        
            if data.email:
                print('help data')
                sent_status=send_query(data.email,ticket_raised)
                print("ticket sent")
                print(sent_status)
                if sent_status == 1:
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})
            else:
                return JsonResponse({'success': False})


    
def send_query(email,ticket_raised):
    """otp_instance = OTP.objects.create(email=email)
    otp_instance.generate_otp()
    otp_instance.save()"""
    support1='jansonalbi2002@gmail.com'
    support2='tharunrangaswamy67@gmail.com'
    try:
        sent_status=send_mail(
            'ReaccelAi Ticket Raised',
            f'ReaccelAi Ticket Raised by{email} issue is:- {ticket_raised}',
            'pinniboinarajesh640@gmail.com',
            [support1,support2],
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

    return sent_status


def creating_iam_user(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', 'default_value')
        form_type = request.POST.get('form_type')
        if form_type == 'creatingiamuser':
            iamname = request.POST.get('iam_username')
            iampassword = request.POST.get('iam_password')
            iamdescription = request.POST.get('iam_description')
            dashboard = request.POST.get('Dashboard')
            modelcreation = request.POST.get('modelcreation')
            performance = request.POST.get('performance')
            acceleration = request.POST.get('acceleration')
            testmodel = request.POST.get('testmodel')
            trackyourself = request.POST.get('trackyourself')
            print(f"iamname={iamname}")
            print(f"iampassword={iampassword}")
            print(f"iamdescription={iamdescription}")
            print(f"dashboard={dashboard}")
            print(f"modelcreation={modelcreation}")
            print(f"performance={performance}")
            print(f"acceleration={acceleration}")
            print(f"testmodel={testmodel}")
            print(f"trackyourself={trackyourself}")

            global accesspermission
            accesspermission=" "
            permissionlist=[dashboard,modelcreation,performance,acceleration,testmodel,trackyourself]

            print(f"permissionlist={permissionlist}")
            for access in permissionlist:
                if access is not None:
                    accesspermission += access + ","
            accesspermission=accesspermission[:-1]
            print(f"access_permissions={accesspermission}")

            if dashboard == "Dashboard":
                dashboard=1 
            else:
                dashboard=0
            
            if modelcreation == "Model Creation":
                modelcreation=1 
            else:
                modelcreation=0
            
            if performance == "Performance":
                performance=1 
            else:
                performance=0

            if acceleration == "Acceleration":
                acceleration=1 
            else:
                acceleration=0

            if testmodel == "Test Model":
                testmodel=1 
            else:
                testmodel=0

            if trackyourself == "Track Your Self":
                trackyourself=1 
            else:
                trackyourself=0

            print(f"dashboard={dashboard}")
            print(f"modelcreation={modelcreation}")
            print(f"performance={performance}")
            print(f"acceleration={acceleration}")
            print(f"testmodel={testmodel}")
            print(f"trackyourself={trackyourself}")
            others=0
            new_user = admin_iam_users(reaccel_id=user_id,iam_user_name=iamname, iam_user_password=iampassword,access_permissions=accesspermission,description=iamdescription,dashboard=dashboard,model_creation=modelcreation,performance=performance,acceleration=acceleration,test_model=testmodel,track_yourself=trackyourself,others=others)
            new_user.save()
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context = {'user': user}
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context = {'user': iamuser}           
    return render(request, "dashboard/createiamuser.html",context)


def remove_iamuser_ajax(request):
    context = {}
    print("remove user")
    if request.method == 'POST':
        
        data = json.loads(request.body)
        iamuser_check = data.get('iam_user_checkbox')
        print(iamuser_check)
        if iamuser_check:
            iam_user = get_object_or_404(admin_iam_users, iam_user_name=iamuser_check)
            deleted_count, _ = iam_user.delete()
            print(deleted_count)
            if deleted_count > 0:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False})
    
    if whologged == 1:
        user_id = request.session.get('user_id', 'default_value')
        user = User_info.objects.get(reaccelai_id=user_id)
        context['user'] = user
    if whologged == 2:
        iamuser = admin_iam_users.objects.get(iam_user_name=iam)
        context['user'] = iamuser
    user_id = request.session.get('user_id', 'default_value')
    data = admin_iam_users.objects.filter(reaccel_id=user_id).values('iam_user_name','iam_user_password', 'access_permissions','user_createdon','description')
    context['data'] = data
    return render(request, "dashboard/iam.html",context)