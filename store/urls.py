from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    
    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
]