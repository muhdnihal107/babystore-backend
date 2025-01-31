from django.urls import path, include
from .views import ProductListView,ProductByCategoryView,CategoryListView,ProductDetailView,ProductEditView,AddProduct,SearchProductsView


urlpatterns = [
    path('list/',ProductListView.as_view(),name='product-list'),
    path('category/',CategoryListView.as_view(),name='category-list'),
    path('category/<int:category_id>',ProductByCategoryView.as_view(),name='product-category'),
    path('<int:pk>',ProductDetailView.as_view(),name='product-detail'), 
    path('edit/<int:pk>',ProductEditView.as_view(),name='product-edit'), 
    path('add/',AddProduct.as_view(),name='product-add'),
    path('search/',SearchProductsView.as_view(),name='product-search'),

]