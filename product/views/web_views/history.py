from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ...models import UserProductHistory
from ...serializers import UserProductHistoryReadSerializer, UserProductHistoryCreateSerializer


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

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        user = request.user

        existing_history = UserProductHistory.objects.filter(
            user=user, product_id=product_id)

        if existing_history.exists():
            existing_history.delete()

        data = {'user': user.id, 'product': product_id}
        serializer = UserProductHistoryCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            read_serializer = UserProductHistoryReadSerializer(
                serializer.instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
