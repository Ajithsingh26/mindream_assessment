"""Students URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from studentmarks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createmark/', views.StudentCreateMark.as_view(), name='StudentCreateMark'),
    path('getmark/', views.GetStudentsMark.as_view(), name='StudentGetMark'),
    path('getallmark/', views.GetStudentTotalMark.as_view(), name='StudentTotalMark'),
    path('getaveragemark/', views.GetAverageMark.as_view(), name='StudentAverageMark')
]
