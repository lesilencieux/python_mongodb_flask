from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class Structure():
    client = MongoClient("localhost", 27017)
    db = client["missions"]
    structures = db["structures"]

    def get_structures(self):
        result = self.structures.find()
        toreturns = []
        # return [str(structure['_id']) for structure in result]

        return result
        # for structure in result:
        #     structure['_id'] = str(structure['_id'])
        #     toreturns.append(structure)
        # return jsonify(toreturns)

    def get_all_codes_of_structures(self):
        result = self.structures.find()
        toreturns = []
        for structure in result:
            toreturns.append(structure['code_structure'])
        return toreturns

    def get_structure(self, structure_id):
        myquery = {"_id": ObjectId(str(structure_id))}
        return self.structures.find_one(myquery)

    def get_structure_by_code(self, code_structure):
        myquery = {"code_structure": code_structure}
        structures = self.structures.find_one(myquery)
        return structures

    def get_structure_by_zone_and_corps(self, zone, corps):
        myquery = {"zone": zone, "corps": corps}
        structures = self.structures.find(myquery)
        toreturns = []
        for structure in structures:
            structure['_id'] = str(structure['_id'])
            toreturns.append(structure)
        return jsonify(toreturns)

    def create_new_structure(self, jsn):
        # Create index on code of structure field to prevent duplicated inserting
        self.structures.create_index([('code_structure', '')], unique=True)
        try:
            self.structures.insert(jsn)
            return True
        except DuplicateKeyError:
            return False

    def update_structure(self, id, newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        self.structures.update_one(query, updated)
        return 'Updated a structure with id %s' % id

    def deleteStructure(self, id):
        query = {"_id": ObjectId(id)}
        if self.structures.delete_one(query):
            return True
        else:
            return False

    def delete_structure_by_code(self, code_structure):
        query = {"code_structure": code_structure}
        if self.structures.remove(query):
            return True
        else:
            return False
