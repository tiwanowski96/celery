"""rekrutacja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from skaner import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.WebsiteListView.as_view(), name='website_list'),
    url(r'^website_list_upload/$', views.WebsiteListUploadView.as_view(), name='website_list_upload'),
    url(r'^website_detail/(?P<id>(\d)+)/$', views.WebsiteDetailView.as_view(), name='website'),
    url(r'^website_category_list/$', views.WebsiteCategoryListView.as_view(), name='website_category_list'),
    url(r'^website_category_form/$', views.WebsiteCategoryAddView.as_view(), name='website_category_form'),
    url(r'^website_form/$', views.WebsiteAddView.as_view(), name='website_form'),
    url(r'^website_list/(?P<id>(\d)+)/$', views.WebsiteListByCategory.as_view(), name='website_list_by_category'),
]
