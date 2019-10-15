from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Qualite():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    qualites = db["qualite"]


    def get_qualites(self):
        result = self.qualites.find()
        toreturns = []
        # return [str(qualite['_id']) for qualite in result]

        return result
        # for qualite in result:
        #     qualite['_id'] = str(qualite['_id'])
        #     toreturns.append(qualite)
        # return jsonify(toreturns)
    def get_all_codes_of_qualites(self):
        result = self.qualites.find()
        toreturns = []
        for qualite in result:
            toreturns.append(qualite['code_qualite'])
        return toreturns

    def get_qualite(self,qualite_id):
        myquery = { "_id": ObjectId(qualite_id) }
        qualites = self.qualites.find(myquery)

        toreturns = []
        for qualite in qualites:
            qualite["_id"] = str(qualite["_id"])
            toreturns.append(qualite)
        return jsonify(toreturns)


    def create_new_qualite(self,jsn):
        # Create index on code of qualite field to prevent duplicated inserting
        self.qualites.create_index([('libelle_qualite', '')], unique=True)
        try:
            self.qualites.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def updatequalite(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.qualites.update_one(query,updated)
        return 'Updated a qualite with id %s' % id

    def deletequalite(self, id):
        query = {"_id": ObjectId(id)}
        self.qualites.delete_one(query)
        return 'Removed a qualite with id %s' % id

    def delete_qualite_by_code(self, code_qualite):
        query = {"code_qualite": code_qualite}
        if self.qualites.remove(query):
            return True
        else:
            return False




