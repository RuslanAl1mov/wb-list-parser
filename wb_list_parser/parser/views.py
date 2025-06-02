from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .tasks import parse_one_product

from .models import Product, ProductCategory, ParserHistory
from .serializers import ProductSerializer, ProductCategorySerializer, ParserHistorySerializer


class ProductListAPIView(generics.ListAPIView):
    """
    GET /api/v1/parser/products/ — список товаров. 
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryListAPIView(generics.ListAPIView):
    """
    GET /api/v1/parser/categories/ — список категорий.
    """
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    

class ParserHistoryListAPIView(generics.ListAPIView):
    """
    GET /api/v1/parser/parser-history/ — история парсинга.
    """
    serializer_class = ParserHistorySerializer
    queryset = ParserHistory.objects.all()


class ProductsParserAPIView(APIView):
    """
    POST /api/v1/parser/parse-products/?articules=123,456
    """

    def post(self, request, *args, **kwargs):
        raw = request.query_params.get("articules", "")
        articules = [x.strip() for x in raw.split(",") if x.strip()]

        if not articules:
            return Response(
                {"detail": "Передайте ?articules=..."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Отправляем каждый артикул отдельно в Celery
        task_ids = [parse_one_product.delay(a).id for a in articules]

        return Response(
            {
                "detail": "Товары добавлены в очередь парсера",
                "task_ids": task_ids,
                "count": len(task_ids),
            },
            status=status.HTTP_202_ACCEPTED,
        )
