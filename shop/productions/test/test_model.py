from django.test import TestCase
from django.utils.text import slugify
from productions.models import Category, Discount, Product, Image


class CategoryModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(category_name='sports')
        discount = Discount.objects.create(type='percent', amount=10)
        product = Product.objects.create(
            name='Test Product',
            brand='Test Brand',
            specifications='Test Specifications',
            category=category,
            price=100,
            discount=discount,
        )
        Image.objects.create(name='Test Image', product_id=product, photo='path/to/image.jpg')

    # test category model

    def test_category_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('category_name').verbose_name
        self.assertEqual(field_label, 'Category')

    def test_category_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('category_name').max_length
        self.assertEqual(max_length, 255)

    def test_category_object_name_is_category_name(self):
        category = Category.objects.get(id=1)
        object_name = f'{category.category_name}'
        self.assertEqual(str(category), object_name)

    # test discount model

    def test_discount_type_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'type')

    def test_discount_amount_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('amount').verbose_name
        self.assertEqual(field_label, 'amount')

    def test_discount_type_max_length(self):
        discount = Discount.objects.get(id=1)
        max_length = discount._meta.get_field('type').max_length
        self.assertEqual(max_length, 255)

    def test_type_field(self):
        discount = Discount.objects.get(type='percent')
        expected_type = 'percent'
        self.assertEqual(discount.type, expected_type)

    def test_amount_field(self):
        discount = Discount.objects.get(type='percent')
        expected_amount = 10
        self.assertEqual(discount.amount, expected_amount)

    def test_str_representation(self):
        discount = Discount.objects.get(type='percent')
        expected_str = str(discount.id)
        self.assertEqual(str(discount), expected_str)

    # test Product model

    def test_name_field(self):
        product = Product.objects.get(name='Test Product')
        expected_name = 'Test Product'
        self.assertEqual(product.name, expected_name)

    def test_slug_field(self):
        product = Product.objects.get(name='Test Product')
        expected_slug = slugify(product.name)
        self.assertEqual(product.slug, expected_slug)

    def test_brand_field(self):
        product = Product.objects.get(name='Test Product')
        expected_brand = 'Test Brand'
        self.assertEqual(product.brand, expected_brand)

    def test_specifications_field(self):
        product = Product.objects.get(name='Test Product')
        expected_specifications = 'Test Specifications'
        self.assertEqual(product.specifications, expected_specifications)

    def test_category_field(self):
        product = Product.objects.get(name='Test Product')
        category = Category.objects.get(category_name='sports')
        self.assertEqual(product.category, category)

    def test_price_field(self):
        product = Product.objects.get(name='Test Product')
        expected_price = 90
        self.assertEqual(product.price, expected_price)

    def test_available_field(self):
        product = Product.objects.get(name='Test Product')
        self.assertTrue(product.available)

    def test_calculate_discount_method(self):
        product = Product.objects.get(name='Test Product')
        expected_discount = 9
        self.assertEqual(product.calculate_discount(), expected_discount)

    def test_calculate_discounted_price_method(self):
        product = Product.objects.get(name='Test Product')
        expected_discounted_price = 81
        product.calculate_discounted_price()
        self.assertEqual(product.price, expected_discounted_price)

    def test_str_method(self):
        product = Product.objects.get(name='Test Product')
        expected_str = 'Test Product'
        self.assertEqual(str(product), expected_str)

    def test_name_field(self):
        image = Image.objects.get(name='Test Image')
        expected_name = 'Test Image'
        self.assertEqual(image.name, expected_name)

    def test_product_id_field(self):
        image = Image.objects.get(name='Test Image')
        product = Product.objects.get(name='Test Product')
        self.assertEqual(image.product_id, product)

    def test_photo_field(self):
        image = Image.objects.get(name='Test Image')
        expected_photo = 'path/to/image.jpg'
        self.assertEqual(image.photo, expected_photo)
