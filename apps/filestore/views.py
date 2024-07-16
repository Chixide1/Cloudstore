from time import sleep
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import UploadFileForm

# Create your views here.
@login_required(login_url="/login")
def dashboard(request):
    form = UploadFileForm()
    files = File.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {"files": files, 'form': form})

@login_required(login_url="/login")
def upload_file(request: HttpRequest):
    if request.htmx and request.method == 'POST' and request.FILES['file']: # type: ignore
        data =  request.FILES['file']
        File.objects.create(file_data=data,
                            file_name=data.name,
                            file_size=data.size,
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
    file = File.objects.get(pk=file_id)
    file.favourite = not file.favourite
    file.save()
    return render(request, "_file-card.html", {"file": file})

@login_required(login_url="/login")
def favourites(request: HttpRequest):
    files = File.objects.filter(user=request.user).filter(favourite=1)
    return render(request, '_favourites.html', {"files": files})

@login_required(login_url="/login")
def all_files(request: HttpRequest):
    files = File.objects.filter(user=request.user)
    return render(request, '_all-files.html', {"files": files})