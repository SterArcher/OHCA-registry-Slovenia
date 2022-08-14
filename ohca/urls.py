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
from django.views.decorators.cache import cache_page

from ohca.views import index

pageCacheTimeout = 24 * 60 * 60

urlpatterns = [
    path('admin/', admin.site.urls),
    path('download/', views.download),
    path('summary/', index.as_view()),
    path('dsz/', views.dsz),
    # path('summary2/', views.http_response),
    path('case/id/', views.case_by_id, name='case'),
    path('case/id/multi/', views.case_by_id_multi, name='case_multi'),
    path('case/dispatch/', views.case_by_disp, name='dispatch'),
    path('case/dispatch/multi/', views.case_by_disp_multi, name='dispatch_multi'),
    path('system/', views.system_view, name='system'),
    path('locale/', views.locale_view, name='locale'),
    # path('autoform/', views.index22),
    # path('', index.as_view())
    path("", cache_page(pageCacheTimeout)(views.new_index), name="index"),
    path("dsz-1-dan", views.form_name_view, name="form_name"),
    path("30-dan", views.second_form_name_view, name="second_form_name"),
    # path("dsz-retro", views.third_form_name_view, name="third_form_name"),
    path("ndsz-1-dan", views.second_first_form_name_view, name="second_first_formpage"),
    # path("ndsz-retro", views.second_third_form_name_view, name="second_third_form_name"),
    # path("test-form", views.test_view, name="test_page")
]
