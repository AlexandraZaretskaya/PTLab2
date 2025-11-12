from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Product

# Главная страница: список товаров
def index(request):
    products = Product.objects.all()  # получаем все товары из базы
    return render(request, 'shop/index.html', {'products': products})

# Функция покупки товара
def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        product.purchase()  # уменьшаем количество товара
        messages.success(request, f'Вы купили {product.name}!')
    except ValidationError:
        messages.error(request, 'Товара недостаточно на складе')  # сообщение об ошибке
    return redirect('shop:index')
