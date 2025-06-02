# parser/tasks.py
from celery import shared_task
from django.db import transaction
from .models import (
    Product,
    ProductCategory,
    ProductParams,
    ProductPhoto,
    ParserHistory,
)
from .parser_module import WBParser


@shared_task
def parse_one_product(articul: str) -> str:
    """Фоновый парсинг одного артикула + запись в ParserHistory."""
    history = ParserHistory.objects.create(articul=articul, is_completed=False)

    try:
        parser = WBParser()
        url  = parser.get_prod_link(articul)
        data = parser.parse_page(url)

        # если WB не вернул данных
        if not data:
            return "empty"

        # ---------- База ----------
        with transaction.atomic():

            # 1. Категория (может быть None)
            category_obj = None
            if (category_name := data.get("category")):
                category_obj, _ = ProductCategory.objects.get_or_create(
                    name=category_name
                )

            # 2. Сам товар
            prod, _ = Product.objects.update_or_create(
                articul=articul,
                defaults={
                    "name": data.get("name", f"Товар {articul}"),
                    "url":  url,
                    "category": category_obj,
                },
            )

            # 3. Характеристики
            chars = data.get("characteristics", {})

            for top_key, maybe_nested in chars.items():
                if isinstance(maybe_nested, dict):
                    for key, val in maybe_nested.items():
                        ProductParams.objects.update_or_create(
                            product=prod,
                            name=f"{top_key} | {key}",
                            defaults={"value": val},
                        )
                else:
                    # плоский ключ → значение
                    ProductParams.objects.update_or_create(
                        product=prod,
                        name=top_key,
                        defaults={"value": maybe_nested},
                    )

            # 4. Фото
            for photo in data.get("photos", []):
                ProductPhoto.objects.get_or_create(
                    product=prod,
                    photo_url=photo,
                )

        # ---------- История ----------
        history.product = prod
        history.is_completed = True
        history.save(update_fields=("product", "is_completed"))
        return f"Product {articul} parsed"

    except Exception:
        history.save(update_fields=("is_completed",))
        raise
