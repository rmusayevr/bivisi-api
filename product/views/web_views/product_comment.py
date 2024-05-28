import django_filters.rest_framework
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from product.models import ProductComment
from product.serializers import ProductCommentCREATESerializer, WebProductCommentSerializer
from services.pagination import InfiniteScrollPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Product Comments only parent comment null
class ParentCommentListAPIView(ListAPIView):
    serializer_class = WebProductCommentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductComment.objects.filter(
                    parent_comment__isnull=True,
                    product__id=product_id
                ).select_related(
                    'user'
                )


class SubCommentListAPIView(ListAPIView):
    serializer_class = WebProductCommentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        parent_comment_id = self.kwargs['parent_comment_id']
        return  ProductComment.objects.filter(
                    parent_comment__id=parent_comment_id,
                ).select_related(
                    'user'
                )


class ProductCommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product', nullable=True),
                'parent_comment': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the parent comment', nullable=True, default=None),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Comment text', nullable=False),
            },
            required=['comment'],
            description="Either 'product' or 'parent_comment' must be provided."
        ),
        responses={
            201: openapi.Response('Created', ProductCommentCREATESerializer),
            400: 'Bad Request'
        }
    )   

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.pk

        if 'product' not in data and 'parent_comment' not in data:
            return Response({"detail": "Either product or parent_comment must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductCommentCREATESerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
