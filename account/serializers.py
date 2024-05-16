from .models import User, PhoneNumber, Subscription
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginTokenSerializer, cls).get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Check the user's status
        if user.status == 'Not Verified':
            raise serializers.ValidationError(
                'Please verify your account with OTP.')

        # Proceed if the user is active
        if user.status == 'Active':
            data.update({'username': user.username, 'email': user.email})
            return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, validators=[validate_password])
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"error": "This email already exists."})
        if User.objects.filter(username__iexact=attrs['username']).exists():
            raise serializers.ValidationError(
                {"error": "This username already exists."})
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if not any(_.isdigit() for _ in attrs['password_confirm']):
            raise serializers.ValidationError(
                {"error": "The password must contain at least 1 number."})
        if not any(_.isupper() for _ in attrs['password_confirm']):
            raise serializers.ValidationError(
                {"error": "There must be at least 1 uppercase letter in the password."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6, required=True)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, validators=[validate_password])
    otp_code = serializers.CharField(max_length=6, required=True)
    # new_password_confirm = serializers.CharField(
    #     write_only=True, required=True, style={"input_type": "password"})

    def validate(self, attrs):
        # if attrs['new_password'] != attrs['new_password_confirm']:
        #     raise serializers.ValidationError(
        #         {"new_password": "Password fields didn't match."})
        if not any(_.isdigit() for _ in attrs['new_password']):
            raise serializers.ValidationError(
                {"error": "The password must contain at least 1 number."})
        if not any(_.isupper() for _ in attrs['new_password']):
            raise serializers.ValidationError(
                {"error": "There must be at least 1 uppercase letter in the password."})
        if attrs["email"]:
            user = User.objects.get(email=attrs["email"])
            if not user:
                raise serializers.ValidationError("User not found!")
            if not user.is_active:
                raise serializers.ValidationError("Email not activated!")
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."})
        if not any(_.isdigit() for _ in attrs['new_password_confirm']):
            raise serializers.ValidationError(
                {"error": "The password must contain at least 1 number."})
        if not any(_.isupper() for _ in attrs['new_password_confirm']):
            raise serializers.ValidationError(
                {"error": "There must be at least 1 uppercase letter in the password."})

        user = self.context['request'].user

        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError(
                {"current_password": "Wrong password."})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class SubscriptionReadSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    follows = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'follows']


class SubscriptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'follows']


class PopularChannelSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count']
