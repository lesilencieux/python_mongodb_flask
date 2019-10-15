from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Destination():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    destinations = db["destinations"]


    def get_destinations(self):
        result = self.destinations.find()
        toreturns = []
        # return [str(destination['_id']) for destination in result]

        return result
        # for destination in result:
        #     destination['_id'] = str(destination['_id'])
        #     toreturns.append(destination)
        # return jsonify(toreturns)
    def get_all_codes_of_destinations(self):
        result = self.destinations.find()
        toreturns = []
        for destination in result:
            toreturns.append(destination['code_destination'])
        return toreturns

    def get_destination(self,destination_id):
        myquery = { "_id": ObjectId(destination_id) }
        destinations = self.destinations.find(myquery)

        toreturns = []
        for destination in destinations:
            destination["_id"] = str(destination["_id"])
            toreturns.append(destination)
        return jsonify(toreturns)

    def get_destination_by_code(self,code_destination):
        myquery = { "code_destination": code_destination}
        destinations = self.destinations.find(myquery)
        return destinations

    def get_destination_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        destinations = self.destinations.find(myquery)
        toreturns = []
        for destination in destinations:
            destination['_id'] = str(destination['_id'])
            toreturns.append(destination)
        return jsonify(toreturns)

    def create_new_destination(self,jsn):
        # Create index on code of destination field to prevent duplicated inserting
        self.destinations.create_index([('ifu_destination', '')], unique=True)
        self.destinations.create_index([('matricule_destination', '')], unique=True)
        try:
            self.destinations.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def updatedestination(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.destinations.update_one(query,updated)
        return 'Updated a destination with id %s' % id

    def deletedestination(self, id):
        query = {"_id": ObjectId(id)}
        self.destinations.delete_one(query)
        return 'Removed a destination with id %s' % id

    def delete_destination_by_code(self, code_destination):
        query = {"code_destination": code_destination}
        if self.destinations.remove(query):
            return True
        else:
            return False




