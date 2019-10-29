from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Agent():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    agents = db["agents"]


    def get_agents(self):
        result = self.agents.find()
        toreturns = []
        # return [str(agent['_id']) for agent in result]

        return result
        # for agent in result:
        #     agent['_id'] = str(agent['_id'])
        #     toreturns.append(agent)
        # return jsonify(toreturns)
    def get_all_codes_of_agents(self):
        result = self.agents.find()
        toreturns = []
        for agent in result:
            toreturns.append(agent['code_agent'])
        return toreturns

    def get_agent(self,agent_id):
        myquery = { "_id": ObjectId(str(agent_id)) }
        return self.agents.find_one(myquery)

    def get_agent_by_code(self,code_agent):
        myquery = { "code_agent": code_agent}
        agents = self.agents.find(myquery)
        return agents

    def get_agent_by_ifu(self,ifu):
        myquery = { "ifu_agent": ifu}
        agents = self.agents.find_one(myquery)
        return agents

    def get_agent_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        agents = self.agents.find(myquery)
        toreturns = []
        for agent in agents:
            agent['_id'] = str(agent['_id'])
            toreturns.append(agent)
        return jsonify(toreturns)

    def create_new_agent(self,jsn):
        # Create index on code of agent field to prevent duplicated inserting
        self.agents.create_index([('ifu_agent', '')], unique=True)
        self.agents.create_index([('matricule_agent', '')], unique=True)
        try:
            self.agents.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def updateagent(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.agents.update_one(query,updated)
        return 'Updated a agent with id %s' % id

    def delete_agent(self, id):
        query = {"_id": ObjectId(id)}
        self.agents.delete_one(query)
        return True

    def delete_agent_by_code(self, code_agent):
        query = {"code_agent": code_agent}
        if self.agents.remove(query):
            return True
        else:
            return False




