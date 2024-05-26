from django.urls import path
from .views import UserHistoryCreateAPIView, UserHistoryDeleteAPIView, UserHistoryListAPIView



urlpatterns = [
    path('user_history_list/', UserHistoryListAPIView.as_view(), name='user_history_list'),
    path('user_history_create/', UserHistoryCreateAPIView.as_view(), name='user_history_create'),
    path('user_history_delete/', UserHistoryDeleteAPIView.as_view(), name='user_history_delete'),

]
