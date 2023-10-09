from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product_list"),
    path("<int:product_id>/", views.ProductView.as_view(), name="product_info"),
]