from rest_framework import serializers
from .models import Application, Interview
from django.contrib.auth.models import User



class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"
        read_only_fields = ("application",)


class ApplicationSerializer(serializers.ModelSerializer):
    interviews = InterviewSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("user",)



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.filter(email=email).first()

        if user:
            # 🔗 LINK: Google user sets a password
            user.set_password(password)
            user.save()
            return user

        # Normal signup
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )
