from django.db import models
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    category_name = models.CharField('Category', max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(self, *args, **kwargs)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    brand = models.CharField(max_length=255)
    specifications = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(self, *args, **kwargs)

    def __str__(self):
        return self.name


class Discount(models.Model):
    type = models.CharField(max_length=255)
    amount = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

