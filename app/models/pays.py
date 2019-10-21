from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Pays():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    payss = db["pays"]


    def get_payss(self):
        result = self.payss.find()
        return result

    def get_all_codes_of_payss(self):
        result = self.payss.find()
        toreturns = []
        for pays in result:
            toreturns.append(pays['code_pays'])
        return toreturns

    def get_pays(self,pays_id):
        myquery = { "_id": ObjectId(pays_id) }
        payss = self.payss.find(myquery)

        toreturns = []
        for pays in payss:
            pays["_id"] = str(pays["_id"])
            toreturns.append(pays)
        return jsonify(toreturns)

    def get_pays_by_code(self,code_pays):
        myquery = { "code_pays": code_pays}
        payss = self.payss.find(myquery)
        return payss

    def get_pays_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        payss = self.payss.find(myquery)
        toreturns = []
        for pays in payss:
            pays['_id'] = str(pays['_id'])
            toreturns.append(pays)
        return jsonify(toreturns)

    def create_new_pays(self,jsn):
        # Create index on code of pays field to prevent duplicated inserting
        self.payss.create_index([('code_numerique_pays', '')], unique=True)
        try:
            self.payss.insert(jsn)
            return True
        except DuplicateKeyError :
            return False


    def updatepays(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.payss.update_one(query,updated)
        return 'Updated a pays with id %s' % id

    def deletepays(self, id):
        query = {"_id": ObjectId(id)}
        self.payss.delete_one(query)
        return 'Removed a pays with id %s' % id

    def delete_pays_by_code(self, code_pays):
        query = {"code_pays": code_pays}
        if self.payss.remove(query):
            return True
        else:
            return False




