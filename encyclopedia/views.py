from django.shortcuts import render

from . import util

from mdutils.mdutils import MdUtils
import os
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new(request):
    if request.method=="POST":
        new_title = request.POST.get("title")
        current_titles = util.list_entries()

        if new_title == "":
            message = "Please provide a title"
            return error(request, message)

        for title in current_titles:
            if new_title.lower() == title.lower():
                message = "Title already exists"
                return error(request, message)

        content = request.POST.get("content")

        mdFile = MdUtils(file_name=new_title)
        mdFile.write(f"# {new_title}")
        mdFile.new_paragraph(content)
        mdFile.create_md_file()

        path = "/workspaces/161247332/CS50w/Django/wiki"
        os.rename(f"{path}/{new_title}.md", f"{path}/entries/{new_title}.md")

        return entry(request, new_title)

    else:
        return render(request, "encyclopedia/new.html")


def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "message": message
    })


def results(request):
    results = []

    if request.method == "POST":
        query = request.POST.get("q")
        titles = util.list_entries()

        for title in titles:
            if query.lower() == title.lower():
                return entry(request, title)

        for title in titles:
            if query.lower() in title.lower():
                results.append(title)

        return render(request, "encyclopedia/results.html", {
            "results": results
        })

    else:
        return index(request)


def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        message = "Page not found"
        return error(request, message)

    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry)
        })


def edit(request, title):
    if request.method=="POST":
        new_title = request.POST.get("title")

        if new_title == "":
            message = "Please provide a title"
            return error(request, message)

        if new_title != title:
            current_titles = util.list_entries()
            for existing_title in current_titles:
                if new_title.lower() == existing_title.lower():
                    message = "Title already exists"
                    return error(request, message)

        content = request.POST.get("content")

        path = "/workspaces/161247332/CS50w/Django/wiki"
        os.remove(f"{path}/entries/{title}.md")

        mdFile = MdUtils(file_name=new_title)
        mdFile.write(content)
        mdFile.create_md_file()

        os.rename(f"{path}/{new_title}.md", f"{path}/entries/{new_title}.md")

        return entry(request, new_title)

    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": content
        })


def random_page(request):
    titles = util.list_entries()

    n = len(titles)
    r = random.randint(0, n-1)
    title = titles[r]

    return entry(request, title)
