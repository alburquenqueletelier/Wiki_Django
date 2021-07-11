from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class busqueda(forms.Form):
    q = forms.CharField(label="Search wiki") 

class new(forms.Form):
    title = forms.CharField(label="Title wiki")
    text = forms.CharField(widget=forms.Textarea)

def index(request, select=None):
    if "search" not in request.session:
        request.session["search"] = []

    context = {
        "entries": util.list_entries(),
        "search_q": busqueda(),
        "search" : request.session["search"],
        "select" : select,
        "see" : None
    }

    if request.method == "POST":
        search_q = busqueda(request.POST)
        if search_q.is_valid():
            q = search_q.cleaned_data['q']
            request.session["search"] = [q]
            return HttpResponseRedirect(reverse("encyclopedia:index", args=request.session["search"]))
        else:
            return render(request, "encyclopedia/index.html", context)
    else:
        if select in context['entries']:
            context["see"] = markdown2.markdown(util.get_entry(select))

    return render(request, "encyclopedia/index.html", context)


def create(request):
    context = {'form': new()}
    if request.method == "POST":
        form = new(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse('encyclopedia:create'))
        else:
            return render(request, "encyclopedia/create.html", context)
    
    return render(request, "encyclopedia/create.html", context)
