from django.urls import path

from . import views

app_name = "hello"
urlpatterns = [
    path("", views.index, name="index"), # when this app is accessed, it runs the index function
    path("brian", views.brian, name="brian"), # when this app is accessed, it runs the index function
    path("<str:name>", views.greet, name="greet") # passes the argument to the greet function 
]