from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, ProductViewSet, AdditionalImageViewSet, KeyWordViewSet, ProductRatingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'products', ProductViewSet)
router.register(r'additional-images', AdditionalImageViewSet)
router.register(r'keywords', KeyWordViewSet)
router.register(r'product-rating', ProductRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
