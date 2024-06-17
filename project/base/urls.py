from django.urls import path, include
from base.views import home,authView,optimiz#styleCSS
from .views import send_otp_ajax
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", home, name="home"),
    path("login/", authView, name="login"),
    path('login/optimization/', optimiz, name='optimization'),
    #path("style/", styleCSS, name="style"),
    path("index/", views.index, name="dashboard"),
    path("login/ModelCreation/", views.ModelCreation, name="ModelCreation"),
    path("Creation/", views.Creation, name="Creation"),
    path("widgets/", views.widgets, name="widgets"),
    path("tables/", views.tables, name="tables"),
    path("testmodel/", views.testmodel, name="testmodel"),
    path("History/", views.History, name="History"),
    path("project_history/", views.project_history, name="project_history"),
    path("my_iam_users/", views.my_iam_users, name="my_iam_users"),
    path("icon-material/", views.icon_material, name="icon-material"),
    path("icon-fontawesome/", views.icon_fontawesome, name="icon-fontawesome"),
    path("elements/", views.elements, name="elements"),
    path("gallery/", views.gallery, name="gallery"),
    path("invoice/", views.invoice, name="invoice"),
    path("chat/", views.chat, name="chat"),
    path('login/send-otp/', views.send_otp_ajax, name='send_otp_ajax'),
    path('login/verify-otp/', views.verify_otp_ajax, name='verify_otp_ajax'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('login/profile_settings/', views.profile_settings, name='profile_settings'),
    path('login/profile_settings/verify_otp_newpassword/', views.verify_otp_newpassword, name='verify_otp_newpassword'),
    path('login/profile_settings/update_password_send_otp_ajax/', views.update_password_send_otp_ajax, name='update_password_send_otp_ajax'),
    path('login/profile_settings/updating_password_profile_settings/', views.updating_password_profile_settings, name='updating_password_profile_settings'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('signup/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='signup'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('helpme/', views.helpme, name='helpme'),
    path('loginhelpme/helpme_send_query/', views.helpme_send_query, name='helpme_send_query'),
    path('creating_iam_user/', views.creating_iam_user, name='creating_iam_user'),
    path('loginmy_iam_users/remove_iamuser_ajax/', views.remove_iamuser_ajax, name='remove_iamuser_ajax'),
    path('process_image/', views.process_image, name='process_image'),
]