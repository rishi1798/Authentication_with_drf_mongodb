from rest_framework.views import APIView
# from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from pymongo import MongoClient
from .utils import hash_password, verify_password, generate_auth_token  # Assuming these utilities are defined
from .models import User, Token,UserProfile
from .auth_decorator import token_required 
from django.http import JsonResponse



# class RegisterAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user_id = serializer.save()

#             if isinstance(user_id, ObjectId):
#                 user_id = str(user_id)

#             return Response({'user_id': user_id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):

    def post(self, request):
        
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not phone or not password:
            return Response({"error": "Phone and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
        db = client.django  # Update with your database name
        user = db.users.find_one({"phone": phone})

        if user is None:
            # Create the user if it does not exist
            hashed_password = hash_password(password)
            user_id = db.users.insert_one({"phone": phone, "password": hashed_password}).inserted_id
            user = db.users.find_one({"_id": user_id})
            UserProfile.create(user_id, **{"other_fields": "your_additional_data"})

        elif not verify_password(password, user['password']):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        existing_token = db.tokens.find_one({"user_id": user['_id']})
        if existing_token:
            token_value = existing_token['token']
        else:
            # Generate a new token
            token_value = generate_auth_token()
            token = Token(user_id=user['_id'], token=token_value)
            token.save()

        return Response({"token": token_value}, status=status.HTTP_200_OK)
    


class ProfileAPIView(APIView):
    @token_required
    def get(self, request):
    
        client = MongoClient('mongodb://localhost:27017/')
        db = client.django
        user_profile = db.user_profiles.find_one({"user_id": request.user_id})
        if not user_profile:
            return JsonResponse({'message': 'Profile not found'}, status=404)

        # Convert MongoDB document to JSON, excluding the ObjectId
        user_profile = convert_objectid_to_string(user_profile)

        return JsonResponse(user_profile, safe=False)
    

class LogoutAPIView(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        
        if not token:
            return Response({'message': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

        client = MongoClient('mongodb://localhost:27017/')
        db = client.django

        # Remove the token from the database
        result = db.tokens.delete_one({"token": token})

        if result.deleted_count:
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid token or already logged out'}, status=status.HTTP_400_BAD_REQUEST)





from bson import ObjectId

def convert_objectid_to_string(value):
    if isinstance(value, ObjectId):
        return str(value)
    elif isinstance(value, dict):
        return {k: convert_objectid_to_string(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_objectid_to_string(v) for v in value]
    return value
