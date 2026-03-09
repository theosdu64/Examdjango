from django.contrib import admin

from .models import Service, Skill, UserSkill

admin.site.register(Skill)
admin.site.register(Service)
admin.site.register(UserSkill)
