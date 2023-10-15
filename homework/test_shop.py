"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # проверки на метод check_quantity
        assert product.check_quantity(500)
        assert not product.check_quantity(1500)

    def test_product_buy(self, product):
        # проверки на метод buy
        product.buy(500)
        assert product.quantity == 500

        product.buy(0)
        assert product.quantity == 500

    def test_product_buy_more_than_available(self, product):
        #  проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1500)


class TestCart:

    def test_cart_add_product(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 2)

        # Проверяем, что продукт добавлен в корзину
        assert product in cart.products
        assert cart.products[product] == 2

    def test_cart_add_existing_product(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 2)

        # Добавляем тот же продукт с другим количеством
        cart.add_product(product, 3)

        # Проверяем, что количество продукта в корзине увеличилось
        assert cart.products[product] == 5

    def test_cart_remove_product(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 2)

        # Удаляем продукт из корзины
        cart.remove_product(product)

        # Проверяем, что продукт удален из корзины
        assert product not in cart.products

    def test_cart_remove_product_with_count(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 5)

        # Удаляем 3 единицы продукта из корзины
        cart.remove_product(product, 3)

        # Проверяем, что количество продукта в корзине уменьшилось
        assert cart.products[product] == 2

    def test_cart_remove_product_with_count_greater_than_available(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 2)

        # Пытаемся удалить 5 единиц продукта из корзины
        cart.remove_product(product, 5)

        # Проверяем, что продукт полностью удален из корзины
        assert product not in cart.products

    def test_cart_clear(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 3)

        # Очищаем корзину
        cart.clear()

        # Проверяем, что корзина пустая
        assert len(cart.products) == 0

    def test_cart_get_total_price(self, product):
        # Создаем корзину и добавляем продукты с разными ценами и количествами
        cart = Cart()
        cart.add_product(product, 2)
        cart.add_product(Product("pen", 50, "This is a pen", 500), 4)
        cart.add_product(Product("notebook", 200, "This is a notebook", 300), 1)

        # Проверяем, что общая стоимость продуктов в корзине правильно вычисляется
        assert cart.get_total_price() == pytest.approx(600)

    def test_cart_buy(self, product):
        # Создаем корзину и добавляем продукты
        cart = Cart()
        cart.add_product(product, 2)
        cart.add_product(Product("pen", 50, "This is a pen", 500), 4)

        # Покупаем продукты
        cart.buy()

        # Проверяем, что корзина пустая после покупки
        assert len(cart.products) == 0

        # Проверяем, что количество продуктов в списке уменьшилось
        assert product.quantity == 998

    def test_cart_buy_insufficient_quantity(self, product):
        # Создаем корзину и добавляем продукт
        cart = Cart()
        cart.add_product(product, 5)

        # Устанавливаем количество продукта на складе меньше, чем в корзине
        product.quantity = 2

        # Пытаемся купить продукты и ожидаем, что будет выброшено исключение ValueError
        with pytest.raises(ValueError):
            cart.buy()
