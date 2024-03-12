from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationRatingViewSet, CategoryViewSet, DeveloperViewSet, ApplicationViewSet, AdditionalImageViewSet, KeyWordViewSet

# Créer un routeur et enregistrer nos viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'developers', DeveloperViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'additional-images', AdditionalImageViewSet)
router.register(r'keywords', KeyWordViewSet)
router.register(r'application-rating', ApplicationRatingViewSet)

# Les URLs générées par le routeur seront inclues dans le schéma de l'API
urlpatterns = [
    path('', include(router.urls)),
]
