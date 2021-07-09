from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:select>", views.show, name="show"),
    path("busqueda", views.search, name="search")
]
