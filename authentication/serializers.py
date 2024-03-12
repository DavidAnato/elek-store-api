from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_photo', 'address']


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def create(self, validated_data):
        # Récupérer le mot de passe non hashé
        password = validated_data.pop('password', None)
        # Créer l'utilisateur en hashant le mot de passe
        user = CustomUser.objects.create(
            **validated_data,
            password=make_password(password) 
        )
        return user

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Spécifiez le champ password en écriture seule
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        # Hasher le mot de passe avant de l'enregistrer dans la base de données
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
