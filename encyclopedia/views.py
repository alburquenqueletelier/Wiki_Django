from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class search(forms.Form):
    search_ = forms.CharField(label="Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show(request, select):
    see = {'select' : select, 'see' : markdown2.markdown(util.get_entry(select))}
    return render(request, "encyclopedia/show.html", see)