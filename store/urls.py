from django.urls import path
from . import views

urlpatterns = [
    # The main store page
    path('', views.store, name='store'),
    # The individual product page
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]