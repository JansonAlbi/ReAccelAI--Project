from django.urls import path, include
from base.views import home,authView,optimiz#styleCSS
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("login/", authView, name="login"),
    path('login/optimization/', optimiz, name='optimization'),
    #path("style/", styleCSS, name="style"),
    path("index/", views.index, name="dashboard"),
    path("ModelCreation/", views.ModelCreation, name="ModelCreation"),
    path("widgets/", views.widgets, name="widgets"),
    path("tables/", views.tables, name="tables"),
    path("grid/", views.grid, name="grid"),
    path("History/", views.History, name="History"),
    path("form-wizard/", views.form_wizard, name="form-wizard"),
    path("buttons/", views.buttons, name="buttons"),
    path("icon-material/", views.icon_material, name="icon-material"),
    path("icon-fontawesome/", views.icon_fontawesome, name="icon-fontawesome"),
    path("elements/", views.elements, name="elements"),
    path("gallery/", views.gallery, name="gallery"),
    path("invoice/", views.invoice, name="invoice"),
    path("chat/", views.chat, name="chat"),

]