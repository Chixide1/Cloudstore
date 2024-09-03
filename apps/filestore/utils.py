from urllib.parse import urlparse
from django.forms import FileField
from django.http import HttpRequest, HttpResponse 

#Global Variables
quota = 1073741824

def getCurrentPath(request: HttpRequest) -> HttpResponse:
    from .views import all_files as a, favourites as f, shared as s
    currentPath = urlparse(request.headers.get("Hx-Current-Url"))
    if currentPath.path == '/favourites/':         
        return f(request)
    elif currentPath.path == '/shared/':
        return s(request)
    else:
        return a(request)

def generate_chunks(data: FileField):
    with data as f:
        for chunk in iter(lambda: f.read(1024), b''):
            yield chunk