from time import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from .models import Service,Skill, UserSkill

def home(request):
    '''Affiche la page d'accueil avec les derniers services acceptés et les compétences disponibles pour l'utilisateur non conecté 
    si l'utilisateur est connecté alors affiche les compétences de l'utilisateur et les compétences disponibles pour lui'''
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
    '''Affiche la page des services avec les services disponibles pour l'utilisateur filtrer selon ces skill 
    et la possibilité de postuler pour un service'''
    user_services = Service.objects.filter(creator=request.user)
    services = Service.objects.filter(
    volunteer__isnull=True,
    skill__in=request.user.userskill_set.values_list('skill', flat=True)
    ).exclude(creator=request.user)
    context = {"services": services,"user_services": user_services}
    return render(request, 'services.html', context)

@login_required
def postulez(request, service_id):
    '''Permet à un utilisateur de postuler pour un service en vérifiant d'abord s'il n'a pas déjà un service à la même date'''
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
    '''Permet à un utilisateur de créer un service en filtrant les compétences uniquement disponibles pour lui'''
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
    '''Affiche la page de l'utilisateur avec les services qu'il a créé et les services pour lesquels 
    il à postulé en les séparant entre les services en attente d'acceptation et les services acceptés'''
    user_services = Service.objects.filter(creator=request.user)
    accepted_services = user_services.filter(volunteer__isnull=False)
    waiting_services = user_services.filter(volunteer__isnull=True)
    volunteer_services = Service.objects.filter(volunteer=request.user)
    context = {"user_services": user_services,"waiting_services": waiting_services, "accepted_services": accepted_services, "volunteer_services": volunteer_services}
    return render(request, 'my_services.html', context)

@login_required
def deleteUserSkill(request, skill_id):
    '''Permet à un utilisateur de supprimer une compétence de son profil'''
    skill = Skill.objects.get(id=skill_id)
    UserSkill.objects.filter(user=request.user, skill=skill).delete()
    return redirect('app:home')

@login_required
def addUserSkill(request, skill_id):
    '''Permet à un utilisateur d'ajouter une compétence à son profil'''
    skill = Skill.objects.get(id=skill_id)
    UserSkill.objects.create(user=request.user, skill=skill)
    return redirect('app:home')

@login_required
def exchange(request):
    user = request.user
    user_skill = UserSkill.objects.filter(user=user).values_list('skill', flat=True)
    user_skill_needed = Service.objects.filter(
        volunteer__isnull=True,
        creator = user,
    ).values_list('skill', flat=True)

    suggested_services = Service.objects.filter(
        volunteer__isnull=True,
        skill__in=user_skill,
        creator__userskill__skill__in=user_skill_needed
    ).exclude(creator=user).distinct()

    if suggested_services.count() > 0:
       other_user = suggested_services.values_list('creator', flat=True)
       other_user_skills = UserSkill.objects.filter(user__in=other_user).values_list('skill', flat=True)  
       other_user_skills_name = UserSkill.objects.filter(user__in=other_user).distinct()
       own_services = Service.objects.filter(
          volunteer__isnull=True,
          creator=user,
          skill__in=other_user_skills 
       ) 

    return render(request, 'exchange.html', {'own_services': own_services, 'other_user_services': suggested_services, 'other_user_skills': other_user_skills , 'other_user_skills_name': other_user_skills_name})