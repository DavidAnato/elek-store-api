from rest_framework import serializers
from .models import Category, Developer, Application, AdditionalImage, KeyWord, ApplicationRating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'

class AdditionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalImage
        fields = '__all__'

class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    additional_image_set = AdditionalImageSerializer(many=True, read_only=True)
    keyword_set = KeyWordSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

    def validate(self, attrs):
        # Récupérer les valeurs des champs
        installation_file = attrs.get('installation_file')
        download_link = attrs.get('download_link')

        # Vérifier si l'un des deux champs est rempli
        if not installation_file and not download_link:
            raise serializers.ValidationError("Vous devez fournir soit un fichier d'installation, soit un lien de téléchargement.")

        return attrs

class ApplicationRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationRating
        fields = ['application', 'rating']
