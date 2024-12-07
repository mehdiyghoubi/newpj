from django.contrib import admin
from .models import *
# Register your models here.
class ProductVariantInline(admin.TabularInline):
    model = Variants
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'create' , 'update')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'amount' , 'unit_price' , 'discount' , 'total_price')
    inlines = [ProductVariantInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product , ProductAdmin)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Variants)