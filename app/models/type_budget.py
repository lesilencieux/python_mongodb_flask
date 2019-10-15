from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class TypeBudget():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    type_budgets = db["type_budgets"]


    def get_type_budgets(self):
        result = self.type_budgets.find()
        toreturns = []
        # return [str(budget['_id']) for budget in result]

        return result
        # for budget in result:
        #     budget['_id'] = str(budget['_id'])
        #     toreturns.append(budget)
        # return jsonify(toreturns)
    def get_all_codes_of_type_budgets(self):
        result = self.type_budgets.find()
        toreturns = []
        for type_budget in result:
            toreturns.append(type_budget['code_type_budget'])
        return toreturns

    def get_budget(self,type_budget_id):
        myquery = { "_id": ObjectId(type_budget_id) }
        type_budgets = self.type_budgets.find(myquery)

        toreturns = []
        for type_budget in type_budgets:
            type_budget["_id"] = str(type_budget["_id"])
            toreturns.append(type_budget)
        return jsonify(toreturns)

    def get_type_budget_by_code(self,code_type_budget):
        myquery = { "code_type_budget": code_type_budget}
        type_budgets = self.type_budgets.find(myquery)
        return type_budgets

    def get_type_budget_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        type_budgets = self.type_budgets.find(myquery)
        toreturns = []
        for type_budget in type_budgets:
            type_budget['_id'] = str(type_budget['_id'])
            toreturns.append(type_budget)
        return jsonify(toreturns)

    def create_new_type_budget(self,jsn):
        # Create index on code of libelle_unique_type_budget field to prevent duplicated inserting
        self.type_budgets.create_index([('libelle_unique_type_budget', '')], unique=True)
        try:
            self.type_budgets.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def updatetype_budget(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.type_budgets.update_one(query,updated)
        return 'Updated a type_budget with id %s' % id

    def deletetype_budget(self, id):
        query = {"_id": ObjectId(id)}
        self.type_budgets.delete_one(query)
        return 'Removed a type_budget with id %s' % id

    def delete_type_budget_by_code(self, code_type_budget):
        query = {"code_type_budget": code_type_budget}
        if self.type_budgets.remove(query):
            return True
        else:
            return False




