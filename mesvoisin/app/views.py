from time import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ServiceForm
from .models import Service,Skill

def home(request):
    last_services_accepted = Service.objects.filter(volunteer_id__isnull=False)[:5]
    all_skill = Skill.objects.all()
    if request.user.is_authenticated:
        user_skill = request.user.userskill_set.values_list('skill__name', flat=True)
    else:
        user_skill = []
    print(user_skill)
    context = {"last_services": last_services_accepted, "all_skill": all_skill, "user_skill": user_skill}
    print(context)
    return render(request, 'home.html', context)

def services(request):
    user_services = Service.objects.filter(creator=request.user)
    services = Service.objects.filter(volunteer_id__isnull=True)
    context = {"services": services,"user_services": user_services}
    return render(request, 'services.html', context)

def postulez(request, service_id):
    service  = Service.objects.get(id=service_id)
    user_services_dates = Service.objects.filter(volunteer_id=request.user).values_list('date', flat=True)
    if service.date in user_services_dates:
        return HttpResponse("Vous avez déjà un service à cette date", status=400)
    
    if service:
        service.volunteer_id = request.user
        service.save()
        return redirect('app:services')
    else:
        return HttpResponse("Erreur lors de la recupération du service", status=404)
   

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
