from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from itertools import chain
from viewNV08C.models import GNSSData
from viewNV08C.models import DriverStatus


def driverDataListView(request):    
    return render(request, 'viewNV08C/driver.html', {'object_list':list(chain(GNSSData.objects.all().order_by("id").reverse()[:1], DriverStatus.objects.all().order_by("id").reverse()[:1]))})

def dbDataListView(request):    
    return render(request, 'viewNV08C/db.html', {'object_list':list(chain(GNSSData.objects.all().order_by("id").reverse()[:1], DriverStatus.objects.all().order_by("id").reverse()[:1]))})

def homeDataListView(request):    
    return render(request, 'viewNV08C/homePage.html', {'object_list':list(chain(GNSSData.objects.all().order_by("id").reverse()[:1], DriverStatus.objects.all().order_by("id").reverse()[:1]))})
