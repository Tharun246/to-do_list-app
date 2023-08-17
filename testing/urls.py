from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('to_do.urls')),
    path('admin/', admin.site.urls),
]
