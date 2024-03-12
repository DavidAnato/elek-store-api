from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .models import Contact, SkillDomain
from .serializers import ContactSerializer, SkillDomainSerializer

class ContactListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['user__username', 'skill_domains__name', 'professions', 'description']  # Filtrer par tous les champs

    def get_queryset(self):
        queryset = Contact.objects.all()

        # Filtrer par professions
        professions = self.request.query_params.get('professions', None)
        if professions:
            queryset = queryset.filter(professions=professions)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Nombre d'éléments par page
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SkillDomainCreateAPIView(generics.ListCreateAPIView):
    queryset = SkillDomain.objects.all()
    serializer_class = SkillDomainSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
