from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('' , views.home, name='home'),
    path('products/' , views.all_products, name='products'),
    path('details/<int:id>/' , views.product_details, name='details'),
    path('category/<slug>/<int:id>/' , views.all_products, name='category'),
    path('like/<int:id>/' , views.product_like, name='product_like'),
    path('unlike/<int:id>/' , views.product_unlike, name='product_unlike'),
]