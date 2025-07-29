from django.db import models
from django.conf import settings
from cart.models import Cart,CartItems
from products.models import Product

class Order(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'
    
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
    cart = models.ForeignKey(Cart,on_delete=models.PROTECT,related_name='order')
    status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default=PENDING)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)  
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orderitems')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('order', 'product')
