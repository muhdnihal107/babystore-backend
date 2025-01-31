from rest_framework import serializers
from .models import Cart,CartItems
from products.serializers import ProductSerializer
from products.models import Product

class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),source='product',write_only=True
    )
# PrimaryKeyRelatedField allows you to validate and handle the relationship by referencing the 
# primary key (here, product_id) instead of requiring a full nested object.
    class Meta:
        model = CartItems
        fields = ['id','product','product_id','quantity']
class CartSerializer(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True,read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id','user','created_at','items','total_items','total_price']
        read_only_fields = ['created_at', 'total_items', 'total_price']
        