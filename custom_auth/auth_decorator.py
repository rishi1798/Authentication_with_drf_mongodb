from functools import wraps
from django.http import JsonResponse
from pymongo import MongoClient
from .models import Token  # Adjust the import as per your project structure

def token_required(f):
    @wraps(f)
    def decorated_function(self,request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'message': 'Token is missing'}, status=401)

        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client.django
            token_data = db.tokens.find_one({"token": token})
            if not token_data:
                return JsonResponse({'message': 'Invalid Token'}, status=401)
            request.user_id = token_data['user_id']
        except:
            return JsonResponse({'message': 'Token is invalid'}, status=401)

        return f(self,request, *args, **kwargs)
    return decorated_function
