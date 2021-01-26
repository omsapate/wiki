from django.shortcuts import render
from django import forms
import random
from . import util
from markdown2 import Markdown

markdown = Markdown() 

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title",required=True, widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))
    textArea = forms.CharField(label='',required=False,widget=forms.Textarea(attrs={'placeholder': 'Enter Page Content'}))

class EditPage(forms.Form):
    textArea = forms.CharField(label='',required=False,widget=forms.Textarea(attrs={'placeholder': 'Enter Page Content'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry_page(request, page_name):
    if util.get_entry(page_name) != None:
        return render(request,"encyclopedia/entry_page.html",{
        "content": markdown.convert( util.get_entry(page_name)),
        "title": page_name,
        "form": SearchForm()
        })
    else: 
        return render(request,"encyclopedia/error_page.html",{
            'message' : "Page does not exist",
            'title' : "Page does not exist",
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

            if files[0].lower() == query and len(files)==1:
                return entry_page(request, query)


            elif len(files)>=1:
                return render(request, 'encyclopedia/searchpage.html',{"entries":files,"form":SearchForm()})

def newpage(request):

    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            data  = util.list_entries()
            
            if title in data:
                return render(request, "encyclopedia/error_page.html",
                {
                    "title" : "Error",
                    "message": "Title already exist! Try New one" ,
                    "form": SearchForm()                
                }
                )
            else:
                textArea = form.cleaned_data['textArea']
                util.save_entry(title, textArea)

                return entry_page(request, title)

    return render(request, "encyclopedia/newpage.html",{"form": SearchForm(), "Newpageform": NewPageForm()})
                

def editpage(request, page_name):
    if request.method=="GET":
        page = util.get_entry(page_name)

        return render(request, 'encyclopedia/edit.html',{
            'form': SearchForm(),
            'edit':EditPage(initial={'textArea': page}),
            'title': page_name
        })

    else:
        form = EditPage(request.POST)

        if form.is_valid():
            textArea = form.cleaned_data['textArea']
            util.save_entry(page_name, textArea)

            return entry_page(request, page_name)

def randompage(request):
    if request.method =="GET":

        data = util.list_entries()

        index = random.randint(0, len(data)-1)

        return entry_page(request,data[index])

