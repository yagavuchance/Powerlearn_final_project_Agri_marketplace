from django.urls import path
from .import views


urlpatterns = [
   path('checkout/', views.checkout, name='checkout'),
   path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

]
