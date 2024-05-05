from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import SliderSerializer
from .models import Slider



# Slider GET & POST
class SliderListCreateAPIView(ListCreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


# Slider GET & PUT & PATCH & DELETE
class SliderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
