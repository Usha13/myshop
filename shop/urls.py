from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="shopHome"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('tracker/', views.tracker, name="tracker"),
    path('product/<int:myid>', views.product, name="product"),
    path('cart', views.cart, name="cart"),
    path('search/', views.search, name="search"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/', views.payment, name="payment"),
    path('handlepayment/', views.handlepayment, name="handlepayment"),
    path('handlepayment2/', views.handlepayment2, name="handlepayment2"),
    path('checkout2/<int:myid>', views.checkout2, name="checkout2"),
]

