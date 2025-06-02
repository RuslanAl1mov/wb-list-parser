from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название категории")

    class Meta:
        verbose_name="Категория товара"
        verbose_name_plural="Категории товаров"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название товара")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="product_category", verbose_name="Категория")
    articul = models.CharField(max_length=50, verbose_name="Артикул товара")
    url = models.URLField(max_length=600, verbose_name="URL карточки товара")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        
    def __str__(self):
        return self.name


class ProductParams(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_params", verbose_name="Товар")
    name = models.CharField(max_length=250, verbose_name="Название характеристики")
    value = models.CharField(max_length=250, verbose_name="Значение характеристики")

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"
        
    def __str__(self):
        return self.name


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_photos", verbose_name="Товар")
    photo_url = models.URLField(max_length=600, verbose_name="URL на фото товара")
    
    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"
    

class ParserHistory(models.Model):
    articul = models.CharField(max_length=50, verbose_name="Артикул товара")
    is_completed = models.BooleanField(verbose_name="Выполнено без ошибок", default=True)
    product = models.ForeignKey(Product, verbose_name="Скаченый продукт", on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "История парсинга"
        verbose_name_plural = "История парсинга"
        