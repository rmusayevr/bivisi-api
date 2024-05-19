from account.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView
from account.serializers import (
    GeneralSettingsSerializer, ProfileInformationSerializer
)



class GeneralSettingsUpdateView(UpdateAPIView):
    queryset = User.objects.filter(status="Active").all()
    serializer_class = GeneralSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.status == "Active":
            return user
        raise PermissionDenied("You do not have permission to perform this action.")


class ProfileInformationUpdateView(UpdateAPIView):
    queryset = User.objects.filter(status="Active").all()
    serializer_class = ProfileInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.status == "Active":
            return user
        raise PermissionDenied("You do not have permission to perform this action.")
