from django.shortcuts import render
import markdown
import random

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entrytxt = convert_md_to_html(entry)

    if entrytxt:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "entrytxt": entrytxt
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "You have searched for a page that does not exist."
        })
    
def search(request):
    if request.method == "POST":
        search_term = request.POST['q']
        html_content = convert_md_to_html(search_term)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "entry": search_term,
                "entrytxt": html_content
            })
        else:
            entry_list = util.list_entries()
            results = []
            for entry in entry_list:
                if search_term.lower() in entry.lower():
                    results.append(entry)

            return render(request, "encyclopedia/search.html", {
                "results": results
                })
        
def new_entry(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        exist = util.get_entry(title)
        if exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "A page already exists for this topic."
            })
        else:
            util.save_entry(title, content)
            converted_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "entry": title,
                "entrytxt": converted_content
            })
    else:
        return render(request, "encyclopedia/new_entry.html")

        
def edit_entry(request, entry):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(entry, content)
        converted_content = convert_md_to_html(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "entrytxt": converted_content
        })
    else:
        entrytxt = util.get_entry(entry)
        return render(request, "encyclopedia/edit_entry.html", {
            "entry": entry,
            "entrytxt": entrytxt
        })

def rand(request):
    entry_list = util.list_entries()
    print(entry_list)
    rand_entry = random.choice(entry_list)
    print(f"The coice is: {rand_entry}")
    content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": rand_entry,
        "entrytxt": content
    })
