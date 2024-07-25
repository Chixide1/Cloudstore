from urllib.parse import urlparse
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