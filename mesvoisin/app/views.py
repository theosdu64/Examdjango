from django.http import HttpResponse
from django.shortcuts import render

from .models import Service

def home(request):
    last_services_accepted = Service.objects.filter(volunteer_id__isnull=False)[:5]
    context = {"last_services": last_services_accepted}
    print(context)
    return render(request, 'home.html', context)
