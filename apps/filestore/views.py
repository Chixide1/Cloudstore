from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import UploadFileForm


# Create your views here.
@login_required(login_url="/login")
def dashboard(request):
    form = UploadFileForm()
    test = [num for num in range(1, 101)]
    return render(request, 'dashboard.html', {"test": test, 'form': form})

def upload_file(request: HttpRequest):
    if request.method == 'POST' and request.FILES['file']:
        data =  request.FILES['file']

        File.objects.create(file_data=data,
                            file_name=data.name,
                            file_size=data.size,
                            user=request.user)
        return HttpResponse
    else:
        return HttpResponseNotAllowed
    
