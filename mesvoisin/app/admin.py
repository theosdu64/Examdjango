from django.contrib import admin

from .models import Service, Skill, UserSkill, Category

admin.site.register(Skill)
admin.site.register(Service)
admin.site.register(UserSkill)
admin.site.register(Category)
