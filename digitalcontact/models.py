from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()

class SkillDomain(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skill_domains = models.ManyToManyField(SkillDomain)
    professions = models.CharField(max_length=100)
    description = CKEditor5Field('Description', config_name='extends', null=True, blank=True)

    def __str__(self):
        return str(self.user)
