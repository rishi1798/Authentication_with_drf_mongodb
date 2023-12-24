import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


# User model
class User:
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password  # This should be hashed

    @staticmethod
    def create(phone, password):
        new_user = {"phone": phone, "password": password}  # Remember to hash the password
        db = MongoClient('mongodb://localhost:27017/')['django']
        return db.users.insert_one(new_user).inserted_id

    @staticmethod
    def find_by_phone(phone):
        db = MongoClient('mongodb://localhost:27017/')['django']
        user_data = db.users.find_one({"phone": phone})
        if user_data:
            return User(**user_data)
        return None


# UserProfile model
class UserProfile:
    def __init__(self, user_id, **other_fields):
        self.user_id = user_id
        self.other_fields = other_fields

    @staticmethod
    def create(user_id, **other_fields):
        new_profile = {
            "user_id": user_id,
            "other_fields": other_fields,
            "created_at": datetime.datetime.now()
        }
        db = MongoClient('mongodb://localhost:27017/')['django']
        return db.user_profiles.insert_one(new_profile).inserted_id

    @staticmethod
    def find_by_user_id(user_id):
        db = MongoClient('mongodb://localhost:27017/')['django']
        profile_data = db.user_profiles.find_one({"user_id": user_id})
        if profile_data:
            return UserProfile(**profile_data)
        return None



# Token model
class Token:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def save(self):
        token_data = {"user_id": self.user_id, "token": self.token}
        db = MongoClient('mongodb://localhost:27017/')['django']
        return db.tokens.insert_one(token_data).inserted_id

    @staticmethod
    def find_by_token(token):
        db = MongoClient('mongodb://localhost:27017/')['django']
        token_data = db.tokens.find_one({"token": token})
        if token_data:
            return Token(**token_data)
        return None
