from django.urls import path
from .import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Dashboard URLs
    path('supplier_dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('farmer_dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
]