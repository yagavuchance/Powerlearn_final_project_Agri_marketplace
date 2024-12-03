from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/add/', views.add_review, name='add_review'),
]
