from django.conf.urls import url
from . import views
from itertools import chain
from django.views.generic import ListView, DetailView
from viewNV08C.models import GNSSData
from viewNV08C.models import DriverStatus


urlpatterns = [
    url(r'^$', views.homeDataListView, name = 'home'),
     #url(r'^driver/',views.driver, name='driver'),
    #url(r'^$', ListView.as_view(queryset=list(chain(GNSSData.objects.all().order_by("-date").reverse()[:1], DriverStatus.objects.all().order_by("id").reverse()[:1])), template_name="viewNV08C/homePage.html")),
    url(r'^db/', views.dbDataListView, name = 'db'),
    url(r'^driver/', views.driverDataListView, name = 'driver')
    ]



