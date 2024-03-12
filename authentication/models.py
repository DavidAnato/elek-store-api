from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from django_ckeditor_5.fields import CKEditor5Field

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=100, unique=True, verbose_name='numéro de téléphone', blank=True, null=True, default=None)
    profile_photo = models.ImageField(upload_to='profile_photos/', verbose_name='photo de profil', blank=True, null=True)
    address = CKEditor5Field('Adresse', config_name='extends')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_photo:
            img = Image.open(self.profile_photo.path)

            width, height = img.size
            if width != height:
                min_side = min(width, height)
                left = (width - min_side) / 2
                top = (height - min_side) / 2
                right = (width + min_side) / 2
                bottom = (height + min_side) / 2

                img = img.crop((left, top, right, bottom))
                img.save(self.profile_photo.path)
    

