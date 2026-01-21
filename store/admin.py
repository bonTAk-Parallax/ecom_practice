from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["img_tag"]
    list_display = ["name", "price", "quantity", "digital", "img_tag"]

    def get_fieldsets(self, request, obj):
        if obj and obj.photo is not None:
            return ((None, {"fields": ("name", "img_tag", "photo", "price", "quantity", "digital")}),)
        return ((None, {"fields": ( "name", "photo", "price", "quantity", "digital")}),)



admin.site.register(Product, ProductAdmin)


