from django.test import TestCase
from orders.models import Address, Order, OrderItem
from core.models import User
from productions.models import Category, Discount, Product


class ModelsTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone='09123456789')
        address = Address.objects.create(state='Test State', city='Test City', street='Test Street', user_id=user)
        order = Order.objects.create(address_id=address, paid=True, user_id=user)
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
        OrderItem.objects.create(order=order, product_id=product, price=10, quantity=2)

    # test Address model

    def test_state_field(self):
        address = Address.objects.get(state='Test State')
        expected_state = 'Test State'
        self.assertEqual(address.state, expected_state)

    def test_city_field(self):
        address = Address.objects.get(state='Test State')
        expected_city = 'Test City'
        self.assertEqual(address.city, expected_city)

    def test_street_field(self):
        address = Address.objects.get(state='Test State')
        expected_street = 'Test Street'
        self.assertEqual(address.street, expected_street)

    def test_user_id_field(self):
        address = Address.objects.get(state='Test State')
        user = User.objects.get(phone='09123456789')
        self.assertEqual(address.user_id, user)

    def test_str_representation(self):
        address = Address.objects.get(state='Test State')
        expected_str = str(address.id)
        self.assertEqual(str(address), expected_str)

    # test Order model

    def test_address_id_field(self):
        order = Order.objects.get(paid=True)
        address = Address.objects.get(state='Test State')
        self.assertEqual(order.address_id, address)

    def test_paid_field(self):
        order = Order.objects.get(paid=True)
        expected_paid = True
        self.assertEqual(order.paid, expected_paid)

    def test_user_id_fields(self):
        order = Order.objects.get(paid=True)
        user = User.objects.get(phone='09123456789')
        self.assertEqual(order.user_id, user)

    def test_str_representations(self):
        order = Order.objects.get(paid=True)
        expected_str = f'Order {order.id}'
        self.assertEqual(str(order), expected_str)

    def test_get_total_cost(self):
        order = Order.objects.get(paid=True)
        expected_total_cost = 20
        self.assertEqual(order.get_total_cost(), expected_total_cost)

    # test OrderItem model

    def test_order_field(self):
        order_item = OrderItem.objects.first()
        order = Order.objects.get(paid=True)
        self.assertEqual(order_item.order, order)

    def test_product_id_field(self):
        order_item = OrderItem.objects.first()
        product = Product.objects.get(name='Test Product')
        self.assertEqual(order_item.product_id, product)

    def test_price_field(self):
        order_item = OrderItem.objects.first()
        expected_price = 10
        self.assertEqual(order_item.price, expected_price)

    def test_quantity_field(self):
        order_item = OrderItem.objects.first()
        expected_quantity = 2
        self.assertEqual(order_item.quantity, expected_quantity)

    def test_str_representationss(self):
        order_item = OrderItem.objects.first()
        expected_str = str(order_item.id)
        self.assertEqual(str(order_item), expected_str)

    def test_get_cost_method(self):
        order_item = OrderItem.objects.first()
        expected_cost = 20
        self.assertEqual(order_item.get_cost(), expected_cost)
