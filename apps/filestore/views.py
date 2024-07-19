from pathlib import Path
from time import sleep
from uuid import UUID, uuid4
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import UploadForm, SearchForm
from django.contrib import messages
from django.core.files.storage import default_storage

quota = 1000000000

# Create your views here.
@login_required(login_url="/login")
def dashboard(request: HttpRequest):
    files = File.objects.filter(user=request.user)
    # files_json = list(File.objects.filter(user=request.user).values())    

    storage_used = 0
    for file in files:
        storage_used += int(file.size)

    context = {"files": files[::-1], 'uploadform': UploadForm(), 'searchform': SearchForm(), 'storage': {'used': storage_used, 'quota': quota}}
    return render(request, 'dashboard.html', context)

@login_required(login_url="/login")
def upload_file(request: HttpRequest):
    if not request.htmx and not request.method == 'POST' and not request.FILES['file']:
        messages.warning(request, "There was an error when trying to upload the file!")
        return dashboard(request)

    data =  request.FILES['file']
    files = File.objects.filter(user=request.user)

    storage_used = 0
    for file in files:
        storage_used += int(file.size)

    if data.size + storage_used > quota:
        messages.error(request, "Couldn't upload as storage quota would be exceeded!")
        return dashboard(request)

    actual_name = data.name
    data.name = str(uuid4())
    File.objects.create(data=data, name=actual_name, size=data.size, type=data.content_type , user=request.user)
    messages.success(request, "File uploaded successfully")
    return dashboard(request)
    
@login_required(login_url="/login")
def favourite_file(request: HttpRequest, file_id: int):
    if not request.htmx:
        return HttpResponseBadRequest()

    file = File.objects.get(pk=file_id)

    if file.user == request.user:
        file.favourite = not file.favourite
        file.save()
        return render(request, "_file-card.html", {"file": file})
    else:
        return HttpResponseForbidden()

@login_required(login_url="/login")
def favourites(request: HttpRequest):   
    if not request.htmx:
        return redirect('/')
    
    files = File.objects.filter(user=request.user).filter(favourite=1)
    return render(request, '_favourites.html', {"files": files[::-1]})

@login_required(login_url="/login")
def all_files(request: HttpRequest):
    if not request.htmx:
        return dashboard(request)
    
    files = File.objects.filter(user=request.user)
    return render(request, '_all-files.html', {"files": files[::-1]})

@login_required(login_url="/login")
def search(request: HttpRequest):
    if not request.htmx and not request.POST:
        return HttpResponseBadRequest()

    query = request.POST.get('query')

    # if not query:
    #     return dashboard(request)
       
    files = File.objects.filter(user=request.user).filter(name__icontains=query)
    return render(request, '_search.html', {"files": files[::-1]})

def download_file(request: HttpRequest, file_id: int, access_key = ''):
    file = File.objects.get(pk=file_id)
    
    if file.user == request.user:
        with file.data as f:
            response = HttpResponse(f.read(), content_type=file.type)
            response['Content-Disposition'] = f"attachment; filename={file.name}"
            return response
    else:
        return HttpResponseForbidden()