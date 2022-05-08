from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("django/", admin.site.urls),
]
