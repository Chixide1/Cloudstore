"""
URL configuration for Cloudstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.users import views as users
from apps.filestore import views as filestore
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

userpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("register/",users.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(),name="logout"),
    path("check-username/", users.check_username, name='check_username')
]

filestorepatterns = [
    path('', filestore.dashboard, name='dashboard'),
    path("upload_file/", filestore.upload_file, name='upload_file'),
    path("favourite_file/<int:file_id>", filestore.favourite_file, name='favourite_file'),
    path("favourites/", filestore.favourites, name='favourites'),
    path("all_files/", filestore.all_files, name='all_files'),
    path("search/", filestore.search, name='search'),
    path("download_file/<int:file_id>", filestore.download_file, name='download_file'),
    path("download_file/<int:file_id>/<uuid:access_key>", filestore.download_file, name='download_file'),
    path("delete_file/<int:file_id>", filestore.delete_file, name='delete_file')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += userpatterns
urlpatterns += filestorepatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)