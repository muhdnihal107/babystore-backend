from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.email
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product')  # Ensure a product can't be duplicated in the same cart
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.email}'s cart"
