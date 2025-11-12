from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.messages import get_messages
from ..models import Product

class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Золотое колье", price=10000, quantity=5
        )

    def test_can_purchase_true(self):
        """Проверяем, что можно купить доступное количество"""
        self.assertTrue(self.product.can_purchase(3))

    def test_purchase_reduces_quantity(self):
        """Проверяем, что количество уменьшается после покупки"""
        self.product.purchase(2)
        self.assertEqual(self.product.quantity, 3)

    def test_purchase_not_enough_stock(self):
        """Проверяем, что нельзя купить больше, чем есть"""
        with self.assertRaises(ValidationError):
            self.product.purchase(10)


class ProductViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Серебряный браслет", price=5000, quantity=3
        )

    def test_index_view_shows_products(self):
        """Проверяем, что главная страница показывает товары"""
        response = self.client.get(reverse('shop:index'))
        self.assertContains(response, "Серебряный браслет")

    def test_buy_product_decreases_quantity(self):
        """Проверяем, что покупка уменьшает количество товара"""
        self.client.get(reverse('shop:buy_product', args=[self.product.pk]), follow=True)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 2)

    def test_buy_product_no_stock_shows_error(self):
        """Проверяем, что при отсутствии товара показывается сообщение"""
        self.product.quantity = 0
        self.product.save()
        response = self.client.get(reverse('shop:buy_product', args=[self.product.pk]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Товара недостаточно на складе" in str(m) for m in messages))
