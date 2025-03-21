from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_particular', 'is_professional']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if not validated_data['email'].strip():
            raise serializers.ValidationError({'email': 'Email is required.'})
        profile_data = validated_data.pop('profile')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile.objects.create(user=user, **profile_data)
        print(profile.id, "ID profile")
        return user
    
    def update(self, instance, validated_data):
        if not validated_data['email'].strip():
            raise serializers.ValidationError({'email': 'Email is required.'})
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise AuthenticationFailed('Invalid credentials.')
        data['user'] = user
        return data