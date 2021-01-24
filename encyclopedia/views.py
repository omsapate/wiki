from django.shortcuts import render
from django import forms

from . import util


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry_page(request, page_name):
    if util.get_entry(page_name) != None:
        return render(request,"encyclopedia/entry_page.html",{
        "content": util.get_entry(page_name),
        "title": page_name,
        "form": SearchForm()
        })
    else: 
        return render(request,"encyclopedia/error_page.html",{
            "content" : page_name,
            "form": SearchForm(),
        })

def search(request):
    if request.method =="POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["query"].lower()
            data  = util.list_entries()

            files = [fname for fname in data if query in fname.lower()]
            # for title in data:
            #     if query in 

            if len(files)>1:
                return render(request, 'encyclopedia/searchpage.html',{"entries":files,"form":SearchForm()})

            elif len(files)==1:
                return entry_page(request, query)
            



            
    