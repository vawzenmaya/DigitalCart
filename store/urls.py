from django.urls import path
from . import views

urlpatterns = [
    # Home / store page
    path('', views.store, name='store'),

    # Category listing (with optional sub/subsub filters via GET params)
    path('category/<slug:category_slug>/', views.category, name='category'),

    # Product detail
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]