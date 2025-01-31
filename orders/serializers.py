from rest_framework import serializers
from .models import Order,OrderItems
from cart.serializers import CartSerializer,CartItemsSerializer
from products.models import Product
from products.serializers import ProductSerializer

class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),source='product',write_only=True
    )
    class Meta:
        model = OrderItems
        fields = ['id', 'product','product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    
    user = serializers.StringRelatedField(read_only=True) 
    cart = CartSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)
    orderitems = OrderItemsSerializer(many=True, read_only=True) 

    class Meta:
        model = Order
        fields = [
            'id','user','cart','orderitems','payment_method','payment_status','payment_amount','total_amount',
            'status','address','created_at','updated_at','first_name','last_name','phone_number',
            'email','state','pincode','razorpay_order_id'
        ]
        
    
    