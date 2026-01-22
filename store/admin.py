from django.contrib import admin
from .models import Product, Order, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["img_tag"]
    list_display = ["name", "price", "quantity", "digital", "img_tag"]

    def get_fieldsets(self, request, obj):
        if obj and obj.photo is not None:
            return ((None, {"fields": ("name", "img_tag", "photo", "price", "quantity", "digital")}),)
        return ((None, {"fields": ( "name", "photo", "price", "quantity", "digital")}),)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["customer"]
    fields = ("customer", "complete")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ["order"]
    list_display = ("item", "item_quantity", "order")
    fields = ("order", "item", "item_quantity")


admin.site.register(Product, ProductAdmin)


