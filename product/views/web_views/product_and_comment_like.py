from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from product.models import Product, ProductComment, ProductCommentLike, UserProductLike



class ToggleProductLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        user_like, created = UserProductLike.objects.get_or_create(user=self.request.user)

        if product in user_like.product.all():
            user_like.product.remove(product)
            product.like_count -= 1
            product.save()
            return Response({'message': 'Product unliked'}, status=status.HTTP_204_NO_CONTENT)
        else:
            user_like.product.add(product)
            product.like_count += 1
            product.save()
            return Response({'message': 'Product liked'}, status=status.HTTP_201_CREATED)


class ToggleProductCommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_comment_id, *args, **kwargs):
        product_comment = get_object_or_404(ProductComment, pk=product_comment_id)
        user_like, created = ProductCommentLike.objects.get_or_create(user=self.request.user)

        if product_comment in user_like.product_comment.all():
            user_like.product_comment.remove(product_comment)
            product_comment.like_count -= 1
            product_comment.save()
            return Response({'message': 'Product comment unliked'}, status=status.HTTP_204_NO_CONTENT)
        else:
            user_like.product_comment.add(product_comment)
            product_comment.like_count += 1
            product_comment.save()
            return Response({'message': 'Product comment liked'}, status=status.HTTP_201_CREATED)
