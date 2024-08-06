from django.urls import path
from .views import NotificationListCreateView, NotificationDetailView, MarkAllAsReadView

urlpatterns = [
    path('notifications/', NotificationListCreateView.as_view(),
         name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(),
         name='notification-detail'),
    path('notifications/mark-all-as-read/',
         MarkAllAsReadView.as_view(), name='mark-all-as-read'),

]
