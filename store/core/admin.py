from django.contrib import admin

from core.models import Category, Product, ProductImage

class ProductImageInLine(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'in_stock')
    inlines = (ProductImageInLine, )

admin.site.register(Category)
