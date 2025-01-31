from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Cart,CartItems
from .serializers import CartItemsSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart,created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        cart,_ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemsSerializer(data = request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            cart_item,created = CartItems.objects.get_or_create(cart=cart,product=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()
            
            return Response(CartSerializer(cart).data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        cart = Cart.objects.filter(user = request.user).first()
        if cart:
            cart.items.all().delete()
        return Response({"message":"cart is cleared"},status=status.HTTP_204_NO_CONTENT)
class QuantityUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request, pk,*args,**kwargs,):
        action = request.data.get('action')
        product_id = request.data.get('product_id')
        if not action or not product_id:
            return Response({"error": "Action or product_id is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist for this user.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItems.objects.get(pk=pk )
        except CartItems.DoesNotExist:
            return Response({'error': 'CartItem not found.'}, status=status.HTTP_404_NOT_FOUND)

        if action == "increment":
            cart_item.quantity += 1
        elif action == "decrement":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()
        return Response({
            'message': 'Cart item updated successfully.',
            'product_id': product_id,
            'new_quantity': cart_item.quantity
        }, status=status.HTTP_200_OK)

        
class RemoveProductCart(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,product_id,pk):
        try:
            cart = get_object_or_404(Cart,user=request.user)
            cart_item = get_object_or_404(CartItems, pk=pk,product_id=product_id)
            cart_item.delete()
            return Response({"product_id": product_id, "pk": pk},status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except CartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart."}, status=status.HTTP_404_NOT_FOUND)
        
class FetchCartUser(APIView):
    def get(self,request,userId):
        cart = get_object_or_404(Cart,user_id=userId)
        try:
            cartItems = CartItems.objects.filter(cart=cart)
            serializer = CartItemsSerializer(cartItems,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"cartitems not found"},status=status.HTTP_404_NOT_FOUND)
        
        
        
        
        
        
        
        
        
        
        
        
        

