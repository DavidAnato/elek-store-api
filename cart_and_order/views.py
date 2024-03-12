from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, Order, CartItem, OrderItem
from .serializers import CartSerializer, OrderSerializer, CartItemSerializer, AddToCartSerializer
from django.shortcuts import get_object_or_404

from django.core.exceptions import ObjectDoesNotExist

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            # Récupérer le panier de l'utilisateur actuellement authentifié
            return Cart.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            # Si le panier n'existe pas, renvoyer une réponse d'erreur
            return Response({"detail": "Le panier de l'utilisateur n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).order_by('-created_at')

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()
        if obj is not None:
            return get_object_or_404(queryset, pk=obj.pk)
        else:
            # Gérer le cas où aucun objet n'est trouvé
            return Response({"detail": "Vous n'avez pas encore de commande."}, status=status.HTTP_404_NOT_FOUND)
class AddToCartView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Vérifiez si l'utilisateur a déjà un panier
        if not hasattr(user, 'cart'):
            # Si l'utilisateur n'a pas de panier, créez-en un
            cart = Cart.objects.create(user=user)
        else:
            cart = user.cart
        # Enregistrez l'article de panier avec le panier approprié
        serializer.save(cart=cart)

class RemoveFromCartView(generics.RetrieveDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart=self.request.user.cart)

class CreateOrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)
        items = cart.items.all()
        
        if items.exists():
            order = Order.objects.create(user=user)
            
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.price)
            
            cart.items.all().delete()
            cart.promo_code = None
            cart.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Le panier de l'utilisateur est vide"}, status=status.HTTP_400_BAD_REQUEST)
