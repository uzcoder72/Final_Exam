from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductEditView, ProductDeleteView,
    CategoryListView, CategoryProductsView, CategoryCreateView, CategoryEditView, CategoryDeleteView,
    AttributeKeyListView, AttributeValueListView,
    CustomTokenObtainPairView, TokenRefreshView,RegisterView, MyTokenObtainPairView, logout_view
)
from .login import login_view
urlpatterns = [
    path('', ProductListView.as_view(), name='all_products'),
    path('categories/', CategoryListView.as_view(), name='all_categories'),
    path('category/<slug:slug>/', CategoryProductsView.as_view(), name='category_detail'),
    path('category/add-category/', CategoryCreateView.as_view(), name='add_category'),
    path('category/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
    path('category/<slug:slug>/edit/', CategoryEditView.as_view(), name='edit_category'),
    path('product/detail/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/edit/', ProductEditView.as_view(), name='edit_product'),
    path('product/<int:id>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('attribute-key/', AttributeKeyListView.as_view(), name='attribute_keys'),
    path('attribute-value/', AttributeValueListView.as_view(), name='attribute_values'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
