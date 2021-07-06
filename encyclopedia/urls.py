from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:select>", views.show, name="show"),
    path("404", views.show, name='404')
]
