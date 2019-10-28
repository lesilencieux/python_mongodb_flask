from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import dateutil.parser
from datetime import datetime as dt
import datetime


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

    def get_mission(self, mission_id):
        myquery = {"_id": ObjectId(mission_id)}
        return self.missions.find_one(myquery)

    def get_mission_by_code(self, code_mission):
        myquery = {"code_mission": code_mission}
        missions = self.missions.find(myquery)
        return missions

    def get_mission_by_zone_and_corps(self, zone, corps):
        myquery = {"zone": zone, "corps": corps}
        missions = self.missions.find(myquery)
        toreturns = []
        for mission in missions:
            mission['_id'] = str(mission['_id'])
            toreturns.append(mission)
        return jsonify(toreturns)

    def create_new_mission(self, jsn):
        # Create index on code of mission field to prevent duplicated inserting
        # self.missions.create_index([('code_mission', '')], unique=True)
        try:
            self.missions.insert(jsn)
            return True
        except DuplicateKeyError:
            return False

    def update_mission(self, id, newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        if self.missions.update(query, updated):
            return True
        else:
            return False

    def validate_mission(self, id):
        query = {"_id": ObjectId(id)}
        newvalues = {"status_mission": "Validee"}
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

    def check_if_agent_has_already_on_mission_for_start_date(self, agent_mission, start_date, end_date):

        query1 = {"date_debut_mission": {'$gte': dateutil.parser.parse(str(start_date)),
                                         '$lt': dateutil.parser.parse(str(end_date))}}

        result1 = self.missions.find(query1)

        for r in result1:
            if str(agent_mission) in r['agents_mission']:
                return True
            else:
                return False

    def check_if_agent_has_already_on_mission_for_end_date(self, agent_mission, start_date, end_date):

        query1 = {"date_fin_mission": {'$gte': dateutil.parser.parse(str(start_date)),
                                       '$lt': dateutil.parser.parse(str(end_date))}}

        result1 = self.missions.find(query1)

        for r in result1:
            if str(agent_mission) in r['agents_mission']:
                return True
            else:
                return False

    def get_mission_by_agent(self, agent):
        missions_for_agent = []
        list_mission = self.missions.find()
        for mission in list_mission:
            if agent in mission['agents_mission']:
                missions_for_agent.append(mission)
        return missions_for_agent

    def chech_mission_for_agent_between_two_dates(self, agent, start_date, end_date):

        d1 = dt.strptime(start_date, "%m/%d/%Y")
        d2 = dt.strptime(end_date, "%m/%d/%Y")
        missions_for_agent = []
        list_mission = self.missions.find()
        for mission in list_mission:
            if agent in mission['agents_mission']:
                missions_for_agent.append(mission)

        for miss in missions_for_agent:

            if (d1 >= miss['date_debut_mission'] >= d1) or (d2 >= miss['date_fin_mission'] >= d1):
                return True
            else:
                return False
