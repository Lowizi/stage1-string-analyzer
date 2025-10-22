
"""
URL configuration for string_analyzer_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from string_analyzer.views import StringsAPI, StringViewSet, NaturalLanguageFilter, home

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'strings', StringViewSet, basename='string')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('strings/', StringsAPI.as_view(), name='strings_api'),  # POST endpoint
    path('api/', include(router.urls)),  # Include router patterns (GET, DELETE for strings)
    path('strings/filter-by-natural-language/', NaturalLanguageFilter.as_view(), name='natural_language_filter'),  # GET filter
    path('home/', home),  # Move home to avoid root conflict
]
