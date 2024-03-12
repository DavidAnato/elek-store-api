from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "marque"
        verbose_name_plural = "marques"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="catégorie")
    name = models.CharField(max_length=150, verbose_name="nom")
    image = models.ImageField(upload_to='product_images/', verbose_name="image")
    image_secondary = models.ImageField(upload_to='product_images/', verbose_name="image secondaire")
    description = CKEditor5Field('Description', config_name='extends')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name="marque")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="prix")
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="prix promo")
    in_promo = models.BooleanField(default=False, verbose_name="en promo")
    is_vedette = models.BooleanField(default=False, verbose_name="Vedette")
    in_stock = models.BooleanField(default=True, verbose_name="en stock")
    is_new = models.BooleanField(default=True, verbose_name="Nouveau")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date de création")
    specification = CKEditor5Field('Specification', config_name='extends', null=True, blank=True)
    warranty_info = CKEditor5Field('Info Garantie', config_name='extends', null=True, blank=True)
    display = models.CharField(max_length=150, verbose_name="Ecran", null=True, blank=True)
    processor_capacity = models.CharField(max_length=150, verbose_name="Processeur", null=True, blank=True)
    camera_quality = models.CharField(max_length=150, verbose_name="Camera", null=True, blank=True)
    memory = models.CharField(max_length=150, verbose_name="Memoire RAM", null=True, blank=True)
    storage_capacity = models.CharField(max_length=150, verbose_name="Capacite memoire", null=True, blank=True)
    graphics = models.CharField(max_length=150, verbose_name="Graphisme", null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name=_("Note moyenne"))

    def update_average_rating(self):
        # Calculer la note moyenne du produit
        average_rating = ProductRating.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            self.average_rating = round(average_rating, 2)
        else:
            self.average_rating = None

    def save(self, *args, **kwargs):
        # Mettre à jour le champ in_promo
        if self.promo_price is None or self.promo_price >= self.price:
            self.in_promo = False
            self.promo_price = None
        else:
            self.in_promo = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("produit")
        verbose_name_plural = _("produits")

class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_image_set', verbose_name="produit")
    image = models.ImageField(upload_to='additional_images/', verbose_name="image supplémentaire")

    def __str__(self):
        return f"Image supplémentaire pour {self.product.name}"

    class Meta:
        verbose_name = "image supplémentaire"
        verbose_name_plural = "images supplémentaires"

class KeyWord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='keyword_set', verbose_name="produit")
    keyword = models.CharField(max_length=100, verbose_name="Mot clé", null=True)

    def __str__(self):
        return f"Mots clés pour {self.product.name}"

    class Meta:
        verbose_name = "Mot clé"
        verbose_name_plural = "Mots clés"

class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Assure qu'un utilisateur ne peut noter qu'une seule fois un produit
