"""ohca URL Configuration

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
from ohca import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('case/id/', views.case_by_id.as_view(), name='case'),
    path('case/id/multi/', views.case_by_id_multi.as_view(), name='case_multi'),
    path('case/dispatch/', views.case_by_disp.as_view(), name='dispatch'),
    path('case/dispatch/multi/', views.case_by_disp_multi.as_view(), name='dispatch_multi'),
    path('system/', views.system_view.as_view(), name='system'),
    path('locale/', views.locale_view.as_view(), name='locale')
]
