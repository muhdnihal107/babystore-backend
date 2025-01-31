from django.urls import path, include
from .views import CartView,QuantityUpdateView,RemoveProductCart,FetchCartUser


urlpatterns = [
    path('list/',CartView.as_view(),name='cart'),
    path('quantity/<int:pk>',QuantityUpdateView.as_view()),
    path('remove/<int:product_id>/<int:pk>', RemoveProductCart.as_view(), name='remove-product'),
    path('user/<int:userId>',FetchCartUser.as_view(),name='user-cartitems'),
]