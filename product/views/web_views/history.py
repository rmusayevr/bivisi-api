from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ...models import UserProductHistory, Product
from ...serializers import UserProductHistoryReadSerializer, UserProductHistoryCreateSerializer
from django.db import transaction


class UserProductHistoryReadAPIView(ListAPIView):
    queryset = UserProductHistory.objects.all()
    serializer_class = UserProductHistoryReadSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        histories = UserProductHistory.objects.filter(
            user=request.user).order_by('-created_at')
        serializer = UserProductHistoryReadSerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProductHistoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserProductHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            product_ids = serializer.validated_data['products']
            user = self.request.user

            with transaction.atomic():
                for product_id in product_ids:
                    product = Product.objects.get(id=product_id)
                    UserProductHistory.objects.create(
                        user=user, product=product)

            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
