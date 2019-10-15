from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class TypeAgent():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    type_agents = db["type_agents"]


    def get_type_agents(self):
        result = self.type_agents.find()
        toreturns = []
        # return [str(type_agent['_id']) for type_agent in result]

        return result
        # for type_agent in result:
        #     type_agent['_id'] = str(type_agent['_id'])
        #     toreturns.append(type_agent)
        # return jsonify(toreturns)
    def get_all_codes_of_type_agents(self):
        result = self.type_agents.find()
        toreturns = []
        for type_agent in result:
            toreturns.append(type_agent['code_type_agent'])
        return toreturns

    def get_type_agent(self,type_agent_id):
        myquery = { "_id": ObjectId(type_agent_id) }
        type_agents = self.type_agents.find(myquery)

        toreturns = []
        for type_agent in type_agents:
            type_agent["_id"] = str(type_agent["_id"])
            toreturns.append(type_agent)
        return jsonify(toreturns)

    def get_type_agent_by_code(self,code_type_agent):
        myquery = { "code_type_agent": code_type_agent}
        type_agents = self.type_agents.find(myquery)
        return type_agents

    def get_type_agent_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        type_agents = self.type_agents.find(myquery)
        toreturns = []
        for type_agent in type_agents:
            type_agent['_id'] = str(type_agent['_id'])
            toreturns.append(type_agent)
        return jsonify(toreturns)

    def create_new_type_agent(self,jsn):
        # Create index on code of type_agent field to prevent duplicated inserting
        self.type_agents.create_index([('libelle_unique_type_agent', '')], unique=True)
        try:
            self.type_agents.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def updatetype_agent(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.type_agents.update_one(query,updated)
        return 'Updated a type_agent with id %s' % id

    def deletetype_agent(self, id):
        query = {"_id": ObjectId(id)}
        self.type_agents.delete_one(query)
        return 'Removed a type_agent with id %s' % id

    def delete_type_agent_by_code(self, code_type_agent):
        query = {"code_type_agent": code_type_agent}
        if self.type_agents.remove(query):
            return True
        else:
            return False




