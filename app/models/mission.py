from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Mission():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    missions = db["missions"]


    def get_missions(self):
        result = self.missions.find()
        toreturns = []
        # return [str(mission['_id']) for mission in result]

        return result
        # for mission in result:
        #     mission['_id'] = str(mission['_id'])
        #     toreturns.append(mission)
        # return jsonify(toreturns)
    def get_all_codes_of_missions(self):
        result = self.missions.find()
        toreturns = []
        for mission in result:
            toreturns.append(mission['code_mission'])
        return toreturns

    def get_mission(self,mission_id):
        myquery = { "_id": ObjectId(mission_id) }
        missions = self.missions.find(myquery)

        toreturns = []
        for mission in missions:
            mission["_id"] = str(mission["_id"])
            toreturns.append(mission)
        return toreturns

    def get_mission_by_code(self,code_mission):
        myquery = { "code_mission": code_mission}
        missions = self.missions.find(myquery)
        return missions

    def get_mission_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        missions = self.missions.find(myquery)
        toreturns = []
        for mission in missions:
            mission['_id'] = str(mission['_id'])
            toreturns.append(mission)
        return jsonify(toreturns)

    def create_new_mission(self,jsn):
        # Create index on code of mission field to prevent duplicated inserting
        # self.missions.create_index([('code_mission', '')], unique=True)
        try:
            self.missions.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def update_mission(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        if self.missions.update(query,updated):
            return True
        else:
            return False

    def validate_mission(self, id):
        query = {"_id": ObjectId(id)}
        newvalues = {"status_mission":"Validee"}
        updated = {"$set": newvalues}
        if self.missions.update(query, updated):
            return True
        else:
            return False

    def delete_mission(self, id):
        query = {"_id": ObjectId(str(id))}
        if self.missions.remove(query):
            return True
        else:
            return False

    def delete_mission_by_code(self, code_mission):
        query = {"code_mission": code_mission}
        if self.missions.remove(query):
            return True
        else:
            return False




