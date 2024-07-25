from .utils import getCurrentPath, quota
from uuid import UUID, uuid4
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import File, Shared
from .forms import UploadForm, SearchForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(["GET"])
@login_required(login_url="/login")
def dashboard(request: HttpRequest):
    files = File.objects.filter(user=request.user)   

    storage_used = 0
    for file in files:
        storage_used += int(file.size)

    context = {"files": files[::-1], 'uploadform': UploadForm(), 'searchform': SearchForm(), 'storage': {'used': storage_used, 'quota': quota}}
    return render(request, 'dashboard.html', context)

@require_http_methods(['POST'])
@login_required(login_url="/login")
def upload_file(request: HttpRequest):
    if not request.htmx and not request.FILES['file']:
        messages.warning(request, "There was an error when trying to upload the file!")
        request.method = "GET"
        return dashboard(request)

    data =  request.FILES['file']
    files = File.objects.filter(user=request.user)

    storage_used = 0
    for file in files:
        storage_used += int(file.size)

    request.method = "GET"

    if data.size + storage_used > quota:
        messages.error(request, "Couldn't upload as storage quota would be exceeded!")
        return dashboard(request)

    actual_name = data.name
    data.name = str(uuid4())
    File.objects.create(data=data, name=actual_name, size=data.size, type=data.content_type , user=request.user)
    messages.success(request, "File uploaded successfully")
    return dashboard(request)

@require_http_methods(["GET"])   
@login_required(login_url="/login")
def favourite_file(request: HttpRequest, file_id: int):
    if not request.htmx:
        return HttpResponseBadRequest()

    file = File.objects.get(pk=file_id)

    if file.user == request.user:
        file.favourite = not file.favourite
        file.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseForbidden()

@require_http_methods(["GET"])
@login_required(login_url="/login")
def favourites(request: HttpRequest):   
    if not request.htmx:
        return redirect('/')
    
    files = File.objects.filter(user=request.user).filter(favourite=1)
    return render(request, '_favourites.html', {"files": files[::-1]})

@require_http_methods(["GET"])
@login_required(login_url="/login")
def all_files(request: HttpRequest):
    if not request.htmx:
        return dashboard(request)
    
    files = File.objects.filter(user=request.user)
    return render(request, '_all-files.html', {"files": files[::-1]})

@require_http_methods(["POST"]) 
@login_required(login_url="/login")
def search(request: HttpRequest):
    if not request.htmx:
        return HttpResponseBadRequest()

    query = request.POST.get('query')
    request.method = "GET"

    if not query:
        return getCurrentPath(request)
       
    files = File.objects.filter(user=request.user).filter(name__icontains=query)
    return render(request, '_search.html', {"files": files[::-1]})

@require_http_methods(["GET"])
def download_file(request: HttpRequest, file_id: int, key: UUID | None = None ):
    file = File.objects.get(pk=file_id)
    shared = Shared.objects.filter(file__id=file_id).first()

    if file.user == request.user:
        with file.data as f:
            response = HttpResponse(f.read(), content_type=file.type)
            response['Content-Disposition'] = f"attachment; filename={file.name}"
            return response
    elif key == shared.access_key:
        shared.access_count += 1
        shared.save()
        print(key, "\n", shared.access_count)
        with file.data as f:
            response = HttpResponse(f.read(), content_type=file.type)
            response['Content-Disposition'] = f"attachment; filename={file.name}"
            return response
    else:
        return HttpResponseForbidden()

@require_http_methods(["DELETE"])
@login_required(login_url="/login")    
def delete_file(request: HttpRequest, file_id: int):
    if not request.htmx:
        return HttpResponseForbidden()
    
    file = File.objects.get(pk=file_id)
    if request.user == file.user:
        file.delete()
        request.method = "GET"
        return dashboard(request)
    else:
        return HttpResponseForbidden()

@require_http_methods(["GET"])  
@login_required(login_url="/login")    
def share_status(request: HttpRequest, file_id: int):
    shared = Shared.objects.filter(file__id=file_id).first()
    base_url = request.get_host()
    file = File.objects.get(pk=file_id)

    if request.user == file.user: 
        return render(request, "_share-modal.html", {'shared': shared, 'base_url': base_url, 'file': file})
    else:
        return HttpResponseForbidden()

@require_http_methods(["GET"])  
@login_required(login_url="/login")    
def share_file(request: HttpRequest, file_id: int):
    shared = Shared.objects.filter(file__id=file_id).first()

    if shared and request.user == (File.objects.get(pk=file_id)).user: 
        shared.delete()
        return share_status(request, file_id)
    elif not shared and request.user == (File.objects.get(pk=file_id)).user:
        Shared.objects.create(file_id=file_id)
        return share_status(request, file_id)
    else:
        return HttpResponseForbidden()

@require_http_methods(["GET"])
@login_required(login_url="/login")
def shared(request: HttpRequest):   
    if not request.htmx:
        return redirect('/')

    shared = File.objects.filter(id__in=Shared.objects.values_list('file__id', flat=True)).filter(user=request.user)
    return render(request, '_shared.html', {"files": shared[::-1]})