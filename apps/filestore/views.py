from time import sleep
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import UploadForm, SearchForm

# Create your views here.
@login_required(login_url="/login")
def dashboard(request: HttpRequest):
    files = File.objects.filter(user=request.user)

    storage_used = 0
    for file in files:
        storage_used += int(file.size)

    context = {"files": files[::-1], 'uploadform': UploadForm(), 'searchform': SearchForm(), 'storage_used': storage_used }
    return render(request, 'dashboard.html', context)

@login_required(login_url="/login")
def upload_file(request: HttpRequest):
    if request.htmx and request.method == 'POST' and request.FILES['file']:
        data =  request.FILES['file']
        File.objects.create(data=data,
                            name=data.name,
                            size=data.size,
                            user=request.user)
        return HttpResponse("""
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="fa-solid fa-circle-check"></i><span class="ps-2">File uploaded successfully.</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        """)
    else:
        return HttpResponse("""
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fa-solid fa-triangle-exclamation"></i><span class="ps-2">Could not upload file.</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        """)
    
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
        return HttpResponseBadRequest()
    
    files = File.objects.filter(user=request.user).filter(favourite=1)
    return render(request, '_favourites.html', {"files": files[::-1]})

@login_required(login_url="/login")
def all_files(request: HttpRequest):
    if not request.htmx:
        return HttpResponseBadRequest()
    
    files = File.objects.filter(user=request.user)
    return render(request, '_all-files.html', {"files": files[::-1]})

@login_required(login_url="/login")
def search(request: HttpRequest):
    if not request.htmx and not request.POST:
        return HttpResponseBadRequest()

    query = request.POST.get('query')
       
    files = File.objects.filter(user=request.user).filter(name__icontains=query)
    return render(request, '_search.html', {"files": files[::-1]})