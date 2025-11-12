from django.urls import path
from . import views

app_name = 'shop'  # namespace для ссылок в шаблонах

urlpatterns = [
    path('', views.index, name='index'),                  # главная страница со списком товаров
    path('buy/<int:pk>/', views.buy_product, name='buy_product'),  # покупка товара
]
