from django.contrib import admin
from .models import Category, Product, AttributeKey, AttributeValue

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']  # Display these fields in the admin list view
    search_fields = ['name', 'slug']  # Add a search bar for these fields
    prepopulated_fields = {"slug": ("name",)}  # Automatically populate the slug field from the name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'primary_image', 'is_liked', 'comment_count', 'all_images',
                    'attributes']
    search_fields = ['name', 'category__name', 'slug']  # Add a search bar for these fields
    list_filter = ['category']  # Add filters for these fields in the sidebar
    prepopulated_fields = {"slug": ("name",)}  # Automatically populate the slug field from the name

    def is_liked(self, obj):
        return obj.is_liked

    def comment_count(self, obj):
        return obj.comments.count()

    def all_images(self, obj):
        return [img.url.url for img in obj.images.all()]

    def attributes(self, obj):
        return ", ".join([f"{attr.key.name}: {attr.value}" for attr in obj.attributes.all()])  # Fix the method

    is_liked.short_description = 'Liked'
    comment_count.short_description = 'Comment Count'
    all_images.short_description = 'All Images'
    attributes.short_description = 'Attributes'

@admin.register(AttributeKey)
class AttributeKeyAdmin(admin.ModelAdmin):
    list_display = ['name']  # Display this field in the admin list view
    search_fields = ['name']  # Add a search bar for this field

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'product']  # Display these fields in the admin list view
    search_fields = ['key__name', 'value', 'product__name']  # Add a search bar for these fields
    list_filter = ['key', 'product']  # Add filters for these fields in the sidebar
