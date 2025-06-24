from django.db import models
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Category(models.Model):
    name_en = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)

    def __str__(self):
        return self.name_en


class Product(models.Model):
    name_en = models.CharField(max_length=200)
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200)
    description_en = models.TextField()
    description_uz = models.TextField()
    description_ru = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_percentage = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_en

    @property
    def discount_price(self):
        if self.discount_percentage:
            return self.price - (self.price * self.discount_percentage / 100)
        return self.price


@receiver(pre_save, sender=Product)
def resize_image(sender, instance, **kwargs):
    if instance.image and instance.pk is None:  # Yangi rasm yuklanganda
        img = Image.open(instance.image)
        img = img.resize((356, 236), Image.Resampling.LANCZOS)
        img.save(instance.image.path)
