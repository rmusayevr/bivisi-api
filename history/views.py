import django_filters.rest_framework
from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from services.pagination import InfiniteScrollPagination
from .models import UserHistory, ProductVideoType
from .serializers import UserHistoryDeleteSerializer, UserHistorySerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# GET LIST USER HISTORY
class UserHistoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ['product_video_type']
    filterset_fields = ['product_video_type__product_type']
    pagination_class = InfiniteScrollPagination
    serializer_class = UserHistorySerializer

    def get_queryset(self):
        user = self.request.user
        return UserHistory.objects.filter(user=user).select_related('product_video_type', 'product_video_type__product')


# CREATE USER HISTORY
class UserHistoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'history': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'product_video_type_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'watch_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        },
                    ),
                ),
            },
            required=['history'],
        ),
        responses={200: 'User history updated successfully.'}
    )

    def post(self, request):
        user = request.user
        data = request.data.get('history', [])

        new_entries = []
        update_entries = []
        product_video_type_ids = [item.get('product_video_type_id') for item in data]
        
        existing_entries = UserHistory.objects.filter(
            user=user, 
            product_video_type_id__in=product_video_type_ids
        )

        existing_entries_dict = {entry.product_video_type_id: entry for entry in existing_entries}

        for item in data:
            product_video_type_id = item.get('product_video_type_id')
            watch_date = parse_datetime(item.get('watch_date'))
            
            if not product_video_type_id or not watch_date:
                continue

            product_video_type = ProductVideoType.objects.get(pk=product_video_type_id)
            
            if product_video_type_id in existing_entries_dict:
                entry = existing_entries_dict[product_video_type_id]
                entry.watch_date = watch_date
                update_entries.append(entry)
            else:
                new_entries.append(
                    UserHistory(
                        user=user,
                        product_video_type=product_video_type,
                        watch_date=watch_date
                    )
                )

        if new_entries:
            UserHistory.objects.bulk_create(new_entries)

        if update_entries:
            UserHistory.objects.bulk_update(update_entries, ['watch_date'])

        return Response({"message": "User history updated successfully."}, status=status.HTTP_200_OK)


# DELETE USER HISTORY
class UserHistoryDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'history': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                ),
            },
            required=['history'],
        ),
        responses={200: 'User history deleted successfully.'}
    )
    def delete(self, request):
        user = request.user
        data = request.data.get('history', [])

        serializer = UserHistoryDeleteSerializer(data=data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        ids_to_delete = [item['id'] for item in validated_data]
        
        UserHistory.objects.filter(
            user=user, 
            id__in=ids_to_delete
        ).delete()

        return Response({"message": "User history deleted successfully."}, status=status.HTTP_200_OK)

