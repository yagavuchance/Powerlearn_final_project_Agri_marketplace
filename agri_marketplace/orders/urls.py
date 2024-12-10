from django.urls import path
from . import views

urlpatterns = [
    path('orders/place/', views.place_order, name='place_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/success/', views.order_success, name='order_success'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('place/<int:delivery_id>/', views.place_order, name='place_order'),


]
