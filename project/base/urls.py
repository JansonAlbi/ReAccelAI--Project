from django.urls import path, include
from base.views import home,authView#styleCSS

urlpatterns = [
    path("", home, name="home"),
    path("login/", authView, name="login"),
    #path("style/", styleCSS, name="style"),
]