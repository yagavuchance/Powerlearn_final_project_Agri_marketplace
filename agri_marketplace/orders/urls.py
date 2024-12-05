from django.urls import path
from . import views

urlpatterns = [
    path('orders/place/', views.place_order, name='place_order'),
    path('<int:order_id>/success/', views.order_success, name='order_success'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),


]
