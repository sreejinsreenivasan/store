from django.urls import path
from .views import AddProductsView, ProductListView, SearchView

app_name = "app"

urlpatterns = [
    path("add-products/", AddProductsView.as_view(), name="addproduct"),
    path("", ProductListView.as_view(), name="productlist"),
    path("search/", SearchView.as_view(), name="search"),
]
