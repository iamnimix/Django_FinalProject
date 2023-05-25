from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from core.models import BaseModel


# Create your models here.


class Category(models.Model):
    category_name = models.CharField(verbose_name=_('نام'), max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_category', verbose_name=_('دسته بندی والد'))
    photo = models.ImageField(verbose_name=_('عکس'), null=True, blank=True, upload_to='productions/')

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save()

    def get_absolute_url(self):
        return reverse("productions:product_list_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name


class Discount(models.Model):
    type = models.CharField(verbose_name=_('نوع'), max_length=255)
    amount = models.PositiveIntegerField(verbose_name=_('مقدار'))

    class Meta:
        verbose_name = _('تخفیف')
        verbose_name_plural = _('تخفیف ها')

    def __str__(self):
        return str(self.id)


class Product(BaseModel):
    name = models.CharField(verbose_name=_('نام'), max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    brand = models.CharField(verbose_name=_('برند'), max_length=255)
    specifications = models.CharField(verbose_name=_('مشخصات'), max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('دسته بندی'))
    price = models.IntegerField(verbose_name=_('قیمت'))
    available = models.BooleanField(verbose_name=_('موجودی'), default=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('تخفیف'))
    main_image = models.ImageField(verbose_name=_('عکس'), upload_to='productions/')

    class Meta:
        ordering = ('name',)
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

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
    name = models.CharField(verbose_name=_('نام'), max_length=255)
    product_id = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE, verbose_name=_('محصول'))
    photo = models.ImageField(verbose_name=_('عکس'), upload_to='productions/')

    class Meta:
        verbose_name = _('عکس')
        verbose_name_plural = _('عکس ها')

    def __str__(self):
        return self

