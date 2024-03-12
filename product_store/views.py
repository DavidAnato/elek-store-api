from rest_framework import viewsets, filters, pagination

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Brand, Product, AdditionalImage, KeyWord, ProductRating
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, AdditionalImageSerializer, KeyWordSerializer, ProductRatingSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category__name', 'name', 'description', 'keyword_set__keyword', 'brand']
    ordering_fields = ['price', 'average_rating']
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer par category et brand
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name=category)
        brand = self.request.query_params.get('brand', None)
        if brand:
            queryset = queryset.filter(brand__name=brand)
        # Filtrer par in_promo
        in_promo = self.request.query_params.get('in_promo', None)
        if in_promo:
            queryset = queryset.filter(in_promo=in_promo)
        # Filtrer par is_new
        is_new = self.request.query_params.get('is_new', None)
        if is_new:
            queryset = queryset.filter(is_new=is_new)

        return queryset


class AdditionalImageViewSet(viewsets.ModelViewSet):
    queryset = AdditionalImage.objects.all()
    serializer_class = AdditionalImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class KeyWordViewSet(viewsets.ModelViewSet):
    queryset = KeyWord.objects.all()
    serializer_class = KeyWordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filtrer les notes de produit par utilisateur connecté
        return ProductRating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ajouter l'utilisateur connecté à la note de produit lors de la création
        serializer.save(user=self.request.user)

    def get_object(self):
        # S'assurer que l'objet de la note de produit appartient à l'utilisateur connecté
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj
