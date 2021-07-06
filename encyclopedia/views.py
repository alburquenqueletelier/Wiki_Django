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
    if request.method == "POST":
        select = search(request.POST)
        if select.is_valid():
            select_ = form.cleaned_data["select_"]
            if select_ in util.list_entries():
                see = {'select' : select_, 'see' : markdown2.markdown(util.get_entry(select_))}
                return render(request, "encyclopedia/show.html", see)
            else:
                return render(request, "encyclopedia/404.html")
        else:
            return HttpResponseRedirect(reverse("wiki:404"))
    else:
        see = {'select' : select, 'see' : markdown2.markdown(util.get_entry(select))}
        return render(request, "encyclopedia/show.html", see)