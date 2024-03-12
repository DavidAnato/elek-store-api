from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Developer, Application, AdditionalImage, KeyWord, ApplicationRating
from .serializers import CategorySerializer, DeveloperSerializer, ApplicationSerializer, AdditionalImageSerializer, KeyWordSerializer, ApplicationRatingSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category__name', 'developer__name', 'name', 'description', 'keyword_set__keyword', 'developer']
    ordering_fields = ['price', 'average_rating']
    ordering = ['category__name']  # Par défaut, trié par nom de catégorie

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer par category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name=category)
        # Filtrer par developer
        developer = self.request.query_params.get('developer', None)
        if developer:
            queryset = queryset.filter(developer=developer)
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

class ApplicationRatingViewSet(viewsets.ModelViewSet):
    queryset = ApplicationRating.objects.all()
    serializer_class = ApplicationRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filtrer les notes de produit par utilisateur connecté
        return ApplicationRating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ajouter l'utilisateur connecté à la note de produit lors de la création
        serializer.save(user=self.request.user)

    def get_object(self):
        # S'assurer que l'objet de la note de produit appartient à l'utilisateur connecté
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj
