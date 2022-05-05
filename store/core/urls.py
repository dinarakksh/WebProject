from django.urls import path
from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register('cart-items', views.CartItemViewSet)
router.register('carts', views.ShoppingCartViewSet)
urlpatterns = router.urls

urlpatterns += [
       path('categories/', views.categories_list),
       path('categories/<int:pk>/', views.get_category),
       path('categories/<int:pk>/products/', views.get_category_products),
       path('products/', views.ProductListAPIView.as_view()),
       path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
]