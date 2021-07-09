from re import search
from django.http.response import HttpResponse
from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class busqueda(forms.Form):
    q = forms.CharField(label="Search wiki")

def index(request):
    context = {
        "entries": util.list_entries(),
        "search_q": busqueda(),
        "search" : request.session["search"]
    }
    if "search" not in request.session:
        request.session["search"] = []
    
    if request.method == "POST":
        search_q = busqueda(request.POST)
        if search_q.is_valid():
            q = search_q.cleaned_data["q"]
            request.session["search"] = [q]
            HttpResponseRedirect(reverse('encyclopedia:show'), args=search)
        else:
            return render(request, "encyclopedia/index.html",{
                "search_q" : search_q
            })
    
    return render(request, "encyclopedia/index.html", context)


def show(request, select):
    see = {'select' : select, 'see' : markdown2.markdown(util.get_entry(select)), "search_q" : busqueda() }
    return render(request, "encyclopedia/show.html", see)

