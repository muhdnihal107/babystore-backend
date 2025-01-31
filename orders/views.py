from django.shortcuts import render
from rest_framework.views import APIView
from .models import Order,OrderItems
from .serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from cart.models import Cart,CartItems
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from razorpay.errors import SignatureVerificationError
from razorpay.utility import __all__
# Create your views here.

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,*args,**kwargs):
        user = request.user
        data = request.data

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "No active cart found for the user."}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = CartItems.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error":"the cart is empty."},status=status.HTTP_404_NOT_FOUND)
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number =data.get('phone_number')
        email = data.get('email')
        state = data.get('state')
        pincode = data.get('pincode')
        address = data.get('address')
        payment_method = data.get('payment_method')
        payment_amount = data.get('payment_amount')

        if not address or not payment_method:
            return Response({"error": "Address and payment method are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not payment_amount or float(payment_amount) <= 0:
            return Response({"error": "A valid payment amount is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            payment = client.order.create({
                'amount': int(float(payment_amount) * 100),  
                'currency': 'INR',
                'payment_capture': 1  
            })
        except razorpay.errors.RazorpayError as e:
            return Response({"error": "Failed to create Razorpay order", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        order = Order.objects.create(
            user=user,
            cart=cart,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            state=state,
            pincode=pincode,
            address=address,
            payment_method=payment_method,
            payment_amount=payment_amount,
            razorpay_order_id=payment['id'],
        )
        
        order_items = [
            OrderItems(order=order, product=item.product, quantity=item.quantity)
            for item in cart_items
        ]
        OrderItems.objects.bulk_create(order_items)
        
        cart_items.delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class RazorpayPaymentVerify(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            return Response({"error": "Missing payment verification details."}, status=status.HTTP_400_BAD_REQUEST)

        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            
            client.utility.verify_payment_signature(params_dict)

            
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_status = 'Completed'  
            order.save()

            return Response({"message": "Payment verified successfully."}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError as e:
            return Response({"error": "Payment signature verification failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
      
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = request.user
        try:
            last_order = Order.objects.filter(user=user).order_by('-created_at').first()
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or you do not have permission to view this order."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(last_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if 'status' not in request.data:
            return Response({"error":"Status field is required"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = request.data['status']
        order.save()
        return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)  

class OrderDlatailedView(APIView):
    def get(self,request,pk):
        try:
            orderdetail = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or you do not have permission to view this order."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(orderdetail)
        return Response(serializer.data, status=status.HTTP_200_OK)
