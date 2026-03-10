from time import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ServiceForm
from .models import Service,Skill

def home(request):
    last_services_accepted = Service.objects.filter(volunteer_id__isnull=False)[:5]
    all_skill = Skill.objects.all()
    context = {"last_services": last_services_accepted, "all_skill": all_skill}
    print(context)
    return render(request, 'home.html', context)

def services(request):
    user_skill = request.user.userskill_set.values_list('skill_id', flat=True)
    print(user_skill)
    services = Service.objects.filter(volunteer_id__isnull=True)
    context = {"services": services}
    return render(request, 'services.html', context)

def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.creator = request.user
            service.save()
            return redirect('app:services')
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})
