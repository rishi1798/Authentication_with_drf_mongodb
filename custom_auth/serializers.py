# from rest_framework import serializers
# from .models import User, UserProfile, Token  # Replace with the correct import path if needed

# # If you have a separate utility for password hashing
# from .utils import hash_password  # Replace with the actual import path of your hash_password function




# class UserSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=20)
#     password = serializers.CharField(write_only=True, max_length=128)

#     def create(self, validated_data):
#         # Hash the password and create the user
#         hashed_password = hash_password(validated_data['password'])
#         return User.create(validated_data['phone'], hashed_password)

#     def validate_phone(self, value):
#         # Optionally add validation for phone number
#         return value

# class UserProfileSerializer(serializers.Serializer):
#     user_id = serializers.CharField(read_only=True)
#     # Define other fields of the user profile
#     # example: full_name = serializers.CharField(max_length=100)

#     def create(self, validated_data):
#         return UserProfile.create(**validated_data)

#     def update(self, instance, validated_data):
#         # Logic to update user profile
#         pass


# class TokenSerializer(serializers.Serializer):
#     token = serializers.CharField(max_length=256)
