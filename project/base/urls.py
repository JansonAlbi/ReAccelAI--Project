from django.urls import path, include
from base.views import home,authView,optimiz#styleCSS
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("login/", authView, name="login"),
    path('optimization/', optimiz, name='optimization'),
    #path("style/", styleCSS, name="style"),
]