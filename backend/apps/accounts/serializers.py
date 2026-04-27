from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role, UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "role", "full_name")

    def get_full_name(self, obj):
        profile = getattr(obj, "userprofile", None)
        if profile and profile.full_name:
            return profile.full_name
        return obj.get_full_name() or obj.username


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True, write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email
    
    def validate(self, attrs):
        full_name = (attrs.get("full_name") or attrs.get("name") or "").strip()
        if not full_name:
            raise serializers.ValidationError({"full_name": ["Full name is required."]})
        attrs["full_name"] = full_name

        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password_confirm and password_confirm != password:
            raise serializers.ValidationError({"password_confirm": ["Passwords do not match."]})

        email = attrs.get("email")
        attrs["username"] = email

        if User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError({"email": ["A user with this email already exists."]})

        temp_user = User(username=email, email=email)
        validate_password(password, user=temp_user)
        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            role=Role.APPLICANT,
        )
        UserProfile.objects.create(
            user=user,
            full_name=validated_data["full_name"],
            email=email,
        )
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        email = attrs.get("email", "").lower().strip()
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }
        return data
