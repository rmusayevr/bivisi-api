from rest_framework.views import APIView
from .models import Wishlist, Basket, BasketItem
from .serializers import WishlistSerializer, BasketSerializer, BasketItemSerializer
from product.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class WishlistAPIView(APIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    http_method_names = ['get', 'post', 'delete']

    def get(self, request, *args, **kwargs):
        obj, created = Wishlist.objects.get_or_create(user = request.user)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        product = Product.objects.filter(pk=product_id).first()
        if product and self.request.user.is_authenticated:
            wishlist1, created = Wishlist.objects.get_or_create(user = request.user)
            wishlist2 = Wishlist.objects.filter(user = request.user).first()
            wishlist2.items.add(product)
            message = {'success': True, 'message' : 'Product added to your wishlist.'}
            return Response(message, status = status.HTTP_201_CREATED)
        message = {'success' : False, 'message': 'You have to log in to add product your wishlist!'}
        return Response(message, status = status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        ProductID = request.data.get('product')
        if ProductID:
            user_wishlist = Wishlist.objects.get(user = self.request.user)
            product = user_wishlist.items.get(id = ProductID)
            user_wishlist.items.remove(product.id)
        message = {'success': True, 'message' : 'Product deleted from your wishlist.'}
        return Response(message, status = status.HTTP_200_OK)

class BasketAPIView(APIView):
    serializer_class = BasketSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, request, *args, **kwargs):    
        obj, created = Basket.objects.get_or_create(user = request.user, is_active=True)
        serializer = self.serializer_class(obj)    
        return Response(serializer.data, status = status.HTTP_200_OK)    
    
    def post(self, request, *args, **kwargs):
        quantity = request.data.get('quantity')
        product_id = request.data.get('product')
        product = Product.objects.filter(pk=product_id).first()
        if product:
            for_basket, created = BasketItem.objects.get_or_create(product = product, user = request.user)
            basket2 = BasketItem.objects.get(product = product, user = request.user)
            basket2.quantity += quantity
            basket2.save()
            basket1, created = Basket.objects.get_or_create(user = request.user, is_active=True)
            basket1.items.add(basket2) 
            arr = []
            for item in basket1.items.all():
                serializer = BasketItemSerializer(item)
                arr.append(serializer.data)
            data = serializer.data
            data["message"] =  {'success' : True, 'message': 'Product was added to basket!', 'items': arr}
            message = {'success': True, 'message' : 'Product added to your card.'}
            return Response(data, status = status.HTTP_201_CREATED)
        message = {'success' : False, 'message': 'You have to log in to add product your basket!'}
        return Response(message, status = status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        ProductDOWN = request.data.get('productDown')
        ProductUP = request.data.get('productUp')
        if ProductDOWN:
            user_basket = BasketItem.objects.get(product=ProductDOWN, user = request.user)
            user_basket.quantity -= 1
            user_basket.save()
            message = {'success': True, 'message' : 'Product has been decreased.'}
            return Response(message, status = status.HTTP_200_OK)
        elif ProductUP:
            user_basket = BasketItem.objects.get(product=ProductUP, user = request.user)
            user_basket.quantity += 1
            user_basket.save()
            message = {'success': True, 'message' : 'Product has been increased.'}
            return Response(message, status = status.HTTP_200_OK)
        

    def delete(self, request, *args, **kwargs):
        ProductID = request.data.get('product')
        if ProductID:
            user_basket = BasketItem.objects.get(product = ProductID, user = request.user)
            user_basket.delete()
            message = {'success': True, 'message' : 'Product has been deleted.'}
            return Response(message, status = status.HTTP_200_OK)
    