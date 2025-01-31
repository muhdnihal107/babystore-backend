from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category,Product
from .serializers import ProductSerializer,CategorySerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class CategoryListView(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductListView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AddProduct(APIView):
    def post(self, request):
        category_data = request.data.get('category')
        print(request.data, 'hloooo')
        
        # Get the category or return a 404 if it does not exist
        category = get_object_or_404(Category, name=category_data)
        
        product_data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "price": request.data.get("price"),
            "image": request.data.get("image"),
            "category": category.id  # Pass the ID of the category
        }

        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductEditView(APIView):
    def patch(self,request,pk):
        product = Product.objects.get(pk=pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)        
class ProductByCategoryView(APIView):
    def get(self,request,category_id):
        if category_id == 0:
            products = Product.objects.all()
        else:
            products =  Product.objects.filter(category_id = category_id)
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)
    
class ProductDetailView(APIView):
    def get(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SearchProductsView(APIView):
    def get(self, request,*args, **kwargs):
        search = request.query_params.get('search', '')  # Fetch 'search' from query params
        if not search:
            return Response(
                {"error": "Search parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = Product.objects.filter(name__icontains=search)  # Case-insensitive search
        if not products.exists():
            return Response(
                {"message": "No products found for the given search term."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

            

