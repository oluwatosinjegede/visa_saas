from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import Role, User, UserProfile
from apps.accounts.serializers import UserSerializer


class AdminUserCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Role.choices)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return email

    def validate(self, attrs):
        temp_user = User(username=attrs['email'], email=attrs['email'])
        validate_password(attrs['password'], user=temp_user)
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password'],
            role=validated_data['role'],
        )
        UserProfile.objects.create(
            user=user,
            full_name=validated_data['full_name'].strip(),
            email=email,
        )
        return user


class AdminUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'role', 'full_name', 'is_active', 'date_joined')

