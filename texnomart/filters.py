import django_filters
from .models import Category, Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'category']

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']
