from werkzeug.security import check_password_hash
from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError



class User():
    client = MongoClient("localhost", 27017)
    db = client["missions"]
    users = db["users"]

    def __init__(self, username):
        self.username = username
        self.email = None

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
        return check_password_hash(password_hash, password)

    def read(self):
        rs = self.users.find()
        result = []
        for user in rs:
            user['_id'] = str(user['_id'])
            result.append(user)
        return jsonify(result)

    def read_by_id(self, utilisateur_id):
        myquery = {"_id": ObjectId(utilisateur_id)}
        users = self.utilisateurs.find(myquery)
        result = []
        for user in users:
            user["_id"] = str(user["_id"])
            result.append(user)
        return jsonify(result)

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
        self.utilisateurs.delete_one(query)
        return 'Removed a user with id %s' % id


