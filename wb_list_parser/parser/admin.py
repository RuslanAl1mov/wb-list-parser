# admin.py

from django.contrib import admin
from .models import (
    ProductCategory,
    Product,
    ProductParams,
    ProductPhoto,
    ParserHistory
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


class ProductParamsInline(admin.TabularInline):
    model = ProductParams
    extra = 1
    fk_name = "product"
    fields = ("name", "value")
    readonly_fields = ()
    verbose_name = "Характеристика"
    verbose_name_plural = "Характеристики"


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1
    fk_name = "product"
    fields = ("photo_url",)
    readonly_fields = ()
    verbose_name = "Фото товара"
    verbose_name_plural = "Фотографии"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "articul", "url")
    search_fields = ("name", "articul")
    ordering = ("name",)
    inlines = [ProductParamsInline, ProductPhotoInline]
    fieldsets = (
        (None, {
            "fields": ("name", "category", "articul", "url"),
        }),
    )


@admin.register(ProductParams)
class ProductParamsAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "value")
    list_filter = ("product",)
    search_fields = ("name", "value")
    ordering = ("product", "name")


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "photo_url")
    list_filter = ("product",)
    search_fields = ("photo_url",)
    ordering = ("product",)


@admin.register(ParserHistory)
class ParserHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "articul", "product", "is_completed")
    search_fields = ("articul", "product__name")
    ordering = ("product__name",)