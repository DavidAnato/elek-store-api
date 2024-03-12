from rest_framework import serializers
from .models import SkillDomain, Contact
from django.contrib.auth import get_user_model

User = get_user_model()

class SkillDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillDomain
        fields = ['id', 'name']

class ContactSerializer(serializers.ModelSerializer):
    skill_domains = serializers.PrimaryKeyRelatedField(many=True, queryset=SkillDomain.objects.all())

    class Meta:
        model = Contact
        fields = ['user', 'skill_domains', 'professions', 'description']
