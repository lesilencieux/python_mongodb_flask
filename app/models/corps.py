from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class Corps():
    client = MongoClient("localhost", 27017)
    db = client["missions"]
    corpss = db["corps"]

    def get_corpss(self):
        result = self.corpss.find()
        toreturns = []
        # return [str(corps['_id']) for corps in result]

        return result
        # for corps in result:
        #     corps['_id'] = str(corps['_id'])
        #     toreturns.append(corps)
        # return jsonify(toreturns)

    def get_all_codes_of_corpss(self):
        result = self.corpss.find()
        toreturns = []
        for corps in result:
            toreturns.append(corps['code_corps'])
        return toreturns

    def get_corps(self, corps_id):
        myquery = {"_id": ObjectId(corps_id)}
        return self.corpss.find_one(myquery)

    def create_new_corps(self, jsn):
        # Create index on code of corps field to prevent duplicated inserting
        self.corpss.create_index([('libelle_corps', '')], unique=True)
        try:
            self.corpss.insert(jsn)
            return True
        except DuplicateKeyError:
            return False

    def update_corps(self, id, newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        if self.corpss.update_one(query, updated):
            return True
        else:
            return False

    def delete_corps(self, id):
        query = {"_id": ObjectId(id)}
        if self.corpss.delete_one(query):
            return True
        else:
            False

    def delete_corps_by_code(self, code_corps):
        query = {"code_corps": code_corps}
        if self.corpss.remove(query):
            return True
        else:
            return False
