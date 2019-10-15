from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Budget():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    budgets = db["budgets"]


    def get_budgets(self):
        result = self.budgets.find()
        toreturns = []
        # return [str(budget['_id']) for budget in result]

        return result
        # for budget in result:
        #     budget['_id'] = str(budget['_id'])
        #     toreturns.append(budget)
        # return jsonify(toreturns)
    def get_all_codes_of_budgets(self):
        result = self.budgets.find()
        toreturns = []
        for budget in result:
            toreturns.append(budget['code_budget'])
        return toreturns

    def get_budget(self,budget_id):
        myquery = { "_id": ObjectId(budget_id) }
        budgets = self.budgets.find(myquery)

        toreturns = []
        for budget in budgets:
            budget["_id"] = str(budget["_id"])
            toreturns.append(budget)
        return jsonify(toreturns)

    def get_budget_by_code(self,code_budget):
        myquery = { "code_budget": code_budget}
        budgets = self.budgets.find(myquery)
        return budgets

    def get_budget_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        budgets = self.budgets.find(myquery)
        toreturns = []
        for budget in budgets:
            budget['_id'] = str(budget['_id'])
            toreturns.append(budget)
        return jsonify(toreturns)

    def create_new_budget(self,jsn):
        # Create index on code of budget field to prevent duplicated inserting
        self.budgets.create_index([('ifu_budget', '')], unique=True)
        self.budgets.create_index([('matricule_budget', '')], unique=True)
        try:
            self.budgets.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def updatebudget(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.budgets.update_one(query,updated)
        return 'Updated a budget with id %s' % id

    def deletebudget(self, id):
        query = {"_id": ObjectId(id)}
        self.budgets.delete_one(query)
        return 'Removed a budget with id %s' % id

    def delete_budget_by_code(self, code_budget):
        query = {"code_budget": code_budget}
        if self.budgets.remove(query):
            return True
        else:
            return False




