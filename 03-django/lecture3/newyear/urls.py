from django.urls import path

from . import views

app_name = "newyear"
urlpatterns = [
    path("", views.index, name="index") # when this app is accessed, it runs the index function
]