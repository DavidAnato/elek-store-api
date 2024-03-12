from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

class Developer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du développeur")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Développeur"
        verbose_name_plural = "Développeurs"

class Application(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie")
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, verbose_name="Développeur")
    name = models.CharField(max_length=150, verbose_name="Nom de l'application")
    image = models.ImageField(upload_to='product_images/', verbose_name="Image principale")
    installation_file = models.FileField(upload_to='installation_files/', verbose_name="Fichier d'installation", null=True, blank=True)
    download_link = models.URLField(verbose_name="Lien de téléchargement", null=True, blank=True, validators=[URLValidator()])
    description = CKEditor5Field('Description', config_name='extends')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix promo")
    in_promo = models.BooleanField(default=False, verbose_name="En promo")
    is_new = models.BooleanField(default=True, verbose_name="Nouvelle application")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name=_("Note moyenne"))

    def update_average_rating(self):
        # Calculer la note moyenne du produit
        average_rating = ApplicationRating.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
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

    def clean(self):
        if not self.installation_file and not self.download_link:
            raise ValidationError(_("Vous devez fournir soit un fichier d'installation, soit un lien de téléchargement."))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("application")
        verbose_name_plural = _("applications")

class KeyWord(models.Model):
    product = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='keyword_set', verbose_name="produit")
    keyword = models.CharField(max_length=100, verbose_name="Mot clé", null=True)

    def __str__(self):
        return f"Mots clés pour {self.product.name}"

    class Meta:
        verbose_name = "Mot clé"
        verbose_name_plural = "Mots clés"

class AdditionalImage(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='additional_image_set', verbose_name="produit")
    image = models.ImageField(upload_to='additional_images/', verbose_name="image supplémentaire")

    def __str__(self):
        return f"Image supplémentaire pour {self.product.name}"

    class Meta:
        verbose_name = "image supplémentaire"
        verbose_name_plural = "images supplémentaires"

class ApplicationRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'application')
