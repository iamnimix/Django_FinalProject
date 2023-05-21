from django.db import models
from django.urls import reverse
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
        super().save()

    def __str__(self):
        return self.category_name


class Discount(models.Model):
    type = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    brand = models.CharField(max_length=255)
    specifications = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    main_image = models.ImageField(upload_to='productions/')

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse("productions:product_detail", args=[self.id, self.slug])

    def calculate_discount(self):
        if self.discount:
            discount_percent = self.discount.amount
            discount_amount = (self.price * discount_percent) / 100

            return discount_amount

    def calculate_discounted_price(self):
        discounted_price = self.price - self.calculate_discount()
        self.price = discounted_price

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.discount and self.discount.id is None:
            self.discount.save()
        else:
            discount = self.calculate_discount()
            if discount:
                self.calculate_discounted_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='productions/')
