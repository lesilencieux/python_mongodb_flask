from werkzeug.security import check_password_hash
from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class Users():
    client = MongoClient("localhost", 27017)
    db = client["missions"]
    users = db["users"]

    def __init__(self, username, email,roles):
        self._roles = roles
        self.username = username
        self._email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        if check_password_hash(password_hash, password):
            return True
        else:
            return False

    def create(self, user):
        try:
            self.users.insert(user)
            return True
        except DuplicateKeyError:
            return False

    def update_user(self, id, newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.users.update_one(query, updated)
        return 'Updated a user with id %s' % id

    def delete_user(self, id):
        query = {"_id": ObjectId(id)}
        self.users.delete_one(query)
        return 'Removed a user with id %s' % id

    def login_user_with_email(self, email):
        query = {"email": email}
        if self.users.find_one(query):
            return self.users.find_one(query)
        else:
            return False

    def get_user_by_email(self, email):
        query = {"email": email}
        return self.users.find_one(query)

    def login_user_with_username(self, username):
        query = {"username": username}
        if self.users.find_one(query):
            return True
        else:
            return False

    def get_user_by_username(self, username):
        query = {"username": username}
        return self.users.find_one(query)

    def create_new_users(self, jsn):
        # Create index on code of agent field to prevent duplicated inserting
        self.users.create_index([('email', '')], unique=True)
        self.users.create_index([('username', '')], unique=True)
        try:
            self.users.insert(jsn)
            return True
        except DuplicateKeyError:
            return False

    def get_username(self):
        return self.username

    def get_roles(self):
        list_roles= []
        for role in self._roles:
            list_roles.append(str(role))
        return list_roles

    def get_email(self):
        return self._email

