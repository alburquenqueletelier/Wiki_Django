from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("New", views.create, name="create"),
    path("<str:select>", views.index, name="index")
]
