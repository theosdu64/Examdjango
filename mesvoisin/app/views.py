from django.http import HttpResponse
from django.shortcuts import render

from .models import Service,Skill

def home(request):
    last_services_accepted = Service.objects.filter(volunteer_id__isnull=False)[:5]
    all_skill = Skill.objects.all()
    context = {"last_services": last_services_accepted, "all_skill": all_skill}
    print(context)
    return render(request, 'home.html', context)
