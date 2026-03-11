from time import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from .models import Service,Skill, UserSkill

def home(request):
    last_services_accepted = Service.objects.filter(volunteer__isnull=False)[:10]    
    all_skill = Skill.objects.all()
    if request.user.is_authenticated:
        user_skill = request.user.userskill_set.values_list('skill__name', flat=True)
    else:
        user_skill = []
    context = {"last_services": last_services_accepted, "all_skill": all_skill, "user_skill": user_skill}
    return render(request, 'home.html', context)

@login_required
def services(request):
    user_services = Service.objects.filter(creator=request.user)
    services = Service.objects.filter(volunteer__isnull=True)
    context = {"services": services,"user_services": user_services}
    return render(request, 'services.html', context)

@login_required
def postulez(request, service_id):
    service  = Service.objects.get(id=service_id)
    user_services_dates = Service.objects.filter(volunteer=request.user).values_list('date', flat=True)
    if service.date in user_services_dates:
        return HttpResponse("Vous avez déjà un service à cette date", status=400)
    
    if service:
        service.volunteer = request.user
        service.save()
        return redirect('app:services')
    else:
        return HttpResponse("Erreur lors de la recupération du service", status=404)
   
@login_required
def create_service(request):
    all_skill = Skill.objects.all()
    user_skill = request.user.userskill_set.values_list('skill__name', flat=True)
    formated_skills = [skill for skill in all_skill if skill.name not in user_skill]
    transform_queryset_skills = Skill.objects.filter(name__in=formated_skills)
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.creator = request.user
            service.save()
            return redirect('app:services')
    else:
        form = ServiceForm()
    form.fields['skill'].queryset = transform_queryset_skills
    return render(request, 'create_service.html', {'form': form})

@login_required
def my_services(request):
    user_services = Service.objects.filter(creator=request.user)
    accepted_services = user_services.filter(volunteer__isnull=False)
    waiting_services = user_services.filter(volunteer__isnull=True)
    volunteer_services = Service.objects.filter(volunteer=request.user)
    context = {"user_services": user_services,"waiting_services": waiting_services, "accepted_services": accepted_services, "volunteer_services": volunteer_services}
    return render(request, 'my_services.html', context)