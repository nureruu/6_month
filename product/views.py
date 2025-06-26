from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Product, Review, Category
from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductWithReviewsSerializer, CategoryWithCountSerializer
from django.db.models import Count

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def list(self, request, *args, **kwargs):
        queryset = Category.objects.annotate(products_count=Count('products'))
        serializer = CategoryWithCountSerializer(queryset, many=True)
        return Response(serializer.data)
    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryWithCountSerializer
        return CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    @action(detail=False, methods=['get'], url_path='reviews')
    def products_with_reviews(self, request):
        products = Product.objects.prefetch_related('reviews').all()
        serializer = ProductWithReviewsSerializer(products, many=True)
        return Response(serializer.data)
class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer