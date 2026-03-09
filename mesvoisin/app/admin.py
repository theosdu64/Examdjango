from django.contrib import admin

from mesvoisin.app.models import Service, Skill, UserSkill

admin.site.register(Skill)
admin.site.register(Service)
admin.site.register(UserSkill)
