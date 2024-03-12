from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from product_store.models  import Product

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    promo_code = models.CharField(max_length=20, null=True, blank=True)

    def total(self):
        return sum(item.total_price() for item in self.items.all())

    def apply_promo_code(self):
        if self.promo_code:
            try:
                promo_code = PromoCode.objects.get(code=self.promo_code, is_valid=True)
                discount = promo_code.discount
                return discount
            except PromoCode.DoesNotExist:
                self.promo_code = None
                self.save()
        return 0

    def final_total(self):
        discount = self.apply_promo_code()
        return self.total() * (1 - discount / 100)

    def discount(self):
        return self.final_total() - self.total()
    
    def __str__(self):
        return f"Pannier de {self.user.first_name} {self.user.last_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField( null=True, blank=True)
    promo_price = models.FloatField( null=True, blank=True)

    def save(self, *args, **kwargs):
        # Mise à jour du prix et du prix promo depuis le produit associé
        self.price = self.product.price
        self.promo_price = self.product.promo_price

        super().save(*args, **kwargs)

    def total_price(self):
        price = self.promo_price or self.price
        if price is not None:
            return self.quantity * price
        return None

    total_price.short_description = 'Total Price'


    def __str__(self):
        return self.product.name

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.FloatField(help_text="Réduction en pourcentage (ex: 10 pour 10%)")
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount}%)"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delivered = models.BooleanField(default=False)  # Ajout du champ is_delivered
    promo_code = models.CharField(max_length=20, null=True, blank=True)

    def total(self):
        return sum(item.total_price() for item in self.items.all())

    def apply_promo_code(self):
        if self.promo_code:
            try:
                promo_code = PromoCode.objects.get(code=self.promo_code, is_valid=True)
                discount = promo_code.discount
                return discount
            except PromoCode.DoesNotExist:
                self.promo_code = None
                self.save()
        return 0

    def final_total(self):
        discount = self.apply_promo_code()
        return self.total() * (1 - discount / 100)

    def discount(self):
        return self.final_total() - self.total()

    def __str__(self):
        return f"Commande de {self.user.first_name} {self.user.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product.name
