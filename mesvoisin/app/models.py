from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='services_crees')
    volunteer_id = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='volunteer')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return {self.title, self.description, self.skill, self.creator, self.volunteer_id, self.date}
    
class UserSkill(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)