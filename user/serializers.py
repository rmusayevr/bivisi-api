from .models import ChannelCategory, User, PhoneNumber, Subscription
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_countries.serializer_fields import CountryField as CountrySerializerField
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


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
        if user.status == 'Not Verified' and not user.is_active:
            raise serializers.ValidationError(
                'Please verify your account with OTP.')

        # Proceed if the user is active
        if user.status == 'Active':
            data.update({
                'username': user.username, 'email': user.email,
                'first_name': user.first_name, 'last_name': user.last_name,
            })
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


class CustomCountryField(CountrySerializerField):
    def to_representation(self, value):
        if value == '':
            return None
        return super().to_representation(value)


class UserDetailSerializer(serializers.ModelSerializer):
    country = CustomCountryField()
    subscribers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions', 'status',
                   'is_superuser', 'is_staff', 'is_active', 'date_joined')

    def get_subscribers_count(self, obj):
        return Subscription.objects.filter(follows=obj).count()


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


class ChannelCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ChannelCategory
        fields = ['id', 'name']


class PhoneNumberReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone', 'user']


class PhoneNumberCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone', 'user']


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


class SubscriptionSerializer(serializers.ModelSerializer):
    in_subscribe = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    follows_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'bio',
                  'cover_image', 'follower_count', 'follows_count', 'in_subscribe']

    def get_in_subscribe(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(follower=request.user, follows=obj).exists()

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_follows_count(self, obj):
        return obj.following.count()


class GeneralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'birthday']


class ProfileInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar',
                  'cover_image', 'bio', 'instagram', 'twitter', 'facebook']


class DeleteAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        email = attrs.get('email')
        password = attrs.get('password')

        if user.email != email:
            raise ValidationError(
                "The email does not match the authenticated user's email.")

        if not user.check_password(password):
            raise ValidationError("The password is incorrect.")

        return attrs

    def delete_account(self):
        request = self.context.get('request')
        user = request.user

        if user:
            user.delete()
        else:
            raise ValidationError(
                "Unable to delete account. Please try again.")

        return {"message": "Account deleted successfully."}
