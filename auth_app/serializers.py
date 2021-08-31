from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields=['id','first_name','last_name','email','password']
        # fields="__all__"
        exclude = ("password",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            if len(password) > 4:
                instance = self.Meta.model(**validated_data)
                instance.set_password(password)
                instance.save()
                return instance
        raise serializers.ValidationError("Password requirements did not match")


class TokenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
