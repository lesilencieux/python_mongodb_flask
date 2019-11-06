from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import dateutil.parser
from datetime import datetime as dt
import datetime


class Object():
    client = MongoClient("localhost", 27017)
    db = client["missions"]
    objects = db["objects"]

    def get_objects(self):
        return self.objects.find()

    def get_object(self, object_id):
        myquery = {"_id": ObjectId(object_id)}
        return self.objects.find_one(myquery)

    def get_object_by_ref_lettre_mission(self, ref_lettre_mission):
        myquery = {"reference_lettre_de_mission": ref_lettre_mission}
        return self.objects.find_one(myquery)

    def chech_object_mission_between_two_dates(self, ref_lettre_mission, start_date, end_date):

        d1 = dt.strptime(start_date, "%m/%d/%Y")
        d2 = dt.strptime(end_date, "%m/%d/%Y")
        object_mission = self.get_object_by_ref_lettre_mission(ref_lettre_mission)

        if (d1 >= object_mission['date_debut_mission'] >= d1) or (d2 >= object_mission['date_fin_mission'] >= d1):
            return True
        else:
            return False

    def get_object_by_zone_and_corps(self, zone, corps):
        myquery = {"zone": zone, "corps": corps}
        objects = self.objects.find(myquery)
        toreturns = []
        for object in objects:
            object['_id'] = str(object['_id'])
            toreturns.append(object)
        return jsonify(toreturns)

    def create_new_object(self, jsn):
        # Create index on reference_lettre_de_mission of object field to prevent duplicated inserting
        self.objects.create_index([('reference_lettre_de_mission', '')], unique=True)
        try:
            self.objects.insert(jsn)
            return True
        except DuplicateKeyError:
            return False

    def update_object(self, id, newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        if self.objects.update(query, updated):
            return True
        else:
            return False

    def validate_object(self, id):
        query = {"_id": ObjectId(id)}
        newvalues = {"status_object": "Validee"}
        updated = {"$set": newvalues}
        if self.objects.update(query, updated):
            return True
        else:
            return False

    def delete_object(self, id):
        query = {"_id": ObjectId(str(id))}
        if self.objects.remove(query):
            return True
        else:
            return False

    def delete_object_by_code(self, code_object):
        query = {"code_object": code_object}
        if self.objects.remove(query):
            return True
        else:
            return False

    def check_if_agent_has_already_on_object_for_start_date(self, agent_object, start_date, end_date):

        query1 = {"date_debut_object": {'$gte': dateutil.parser.parse(str(start_date)),
                                         '$lt': dateutil.parser.parse(str(end_date))}}

        result1 = self.objects.find(query1)

        for r in result1:
            if str(agent_object) in r['agents_object']:
                return True
            else:
                return False

    def check_if_agent_has_already_on_object_for_end_date(self, agent_object, start_date, end_date):

        query1 = {"date_fin_object": {'$gte': dateutil.parser.parse(str(start_date)),
                                       '$lt': dateutil.parser.parse(str(end_date))}}

        result1 = self.objects.find(query1)

        for r in result1:
            if str(agent_object) in r['agents_object']:
                return True
            else:
                return False

    def get_object_by_agent(self, agent):
        objects_for_agent = []
        list_object = self.objects.find()
        for object in list_object:
            if agent in object['agents_object']:
                objects_for_agent.append(object)
        return objects_for_agent

    def chech_object_for_agent_between_two_dates(self, agent, start_date, end_date):

        d1 = dt.strptime(start_date, "%m/%d/%Y")
        d2 = dt.strptime(end_date, "%m/%d/%Y")
        objects_for_agent = []
        list_object = self.objects.find()
        for object in list_object:
            if agent in object['agents_object']:
                objects_for_agent.append(object)

        for miss in objects_for_agent:

            if (d1 >= miss['date_debut_object'] >= d1) or (d2 >= miss['date_fin_object'] >= d1):
                return True
            else:
                return False
