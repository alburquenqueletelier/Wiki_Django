from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random #Used in layout template#
from django.contrib import messages

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
    entries_l = [entries_l.lower() for entries_l in context['entries']]
    if request.method == "POST":
        search_q = busqueda(request.POST)
        if search_q.is_valid():
            q = search_q.cleaned_data['q']
            request.session["search"] = [q]
            return HttpResponseRedirect(reverse("encyclopedia:index", args=request.session["search"]))
        else:
            return render(request, "encyclopedia/index.html", context)
    elif select:
        select_l = select.lower()
        if select_l in entries_l:
            index = entries_l.index(select_l)        
            context["see"] = markdown2.markdown(util.get_entry(context["entries"][index]))
        else:
            lista = []
            for x in entries_l:
                if select_l in x and len(select_l)/len(x) >= 2/3:
                    lista.append(context["entries"][entries_l.index(x)])
            if lista:
                context["entries"] = lista
                context["see"] = 'Search'
        
    return render(request, "encyclopedia/index.html", context)


def create(request):
    context = {'form': new(),
                'entries':util.list_entries(),
                'error':None
    }
    entries_l = [entries_l.lower() for entries_l in context['entries']]
    if request.method == "POST":
        form = new(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            if title.lower() not in entries_l:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse('encyclopedia:index', kwargs={'select':title}))
            else:
                context["error"] = f"Title '{title}' in use: please change this"

    return render(request, "encyclopedia/create.html", context)

def edit(request, select):
    title = select
    text = util.get_entry(title)
    editor = new({'title':select, 'text':text})
    entries = util.list_entries()
    entries_l = [entries_l.lower() for entries_l in entries]

    context = {
        'edit': editor,
        'error': None,
        'entries':entries,
        'form': editor,
        'select': select
    }

    if request.method == "POST":
        form = new(request.POST)
        if form.is_valid():
            title_f = form.cleaned_data['title']
            text_f = form.cleaned_data['text']
            if title_f.lower() not in entries_l:
                util.save_entry(title_f, text_f)
                context["error"] = None
                return HttpResponseRedirect(reverse('encyclopedia:index'))
            elif title_f.lower() == title.lower():
                util.save_entry(title_f, text_f)
                context["error"] = None
                return HttpResponseRedirect(reverse('encyclopedia:index'))
            else:
                context["error"] = f"{title_f.lower() == title.lower()}"
    
    return render(request, "encyclopedia/edit.html", context)
