from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class Ville():

    client = MongoClient("localhost", 27017)
    db = client["missions"]
    villes = db["ville"]


    def get_villes(self):
        result = self.villes.find()
        return result

    def get_all_codes_of_villes(self):
        result = self.villes.find()
        toreturns = []
        for ville in result:
            toreturns.append(ville['code_ville'])
        return toreturns

    def get_ville(self,ville_id):
        myquery = { "_id": ObjectId(ville_id) }
        return self.villes.find_one(myquery)


    def get_all_cities_for_countries(self, list_contries):
        toreturns = []
        print("*************************** this is ")
        curentry_to_returns = []
        for country in list_contries:
            curentry_to_returns["country"] = country
            query= {"libelle_fr_pays":country}
            cities_of_country =self.villes.find(query)
            curentry_to_returns.append(cities_of_country)
            toreturns.append(curentry_to_returns)
        return toreturns

    def get_ville_by_code(self,code_ville):
        myquery = { "code_ville": code_ville}
        villes = self.villes.find(myquery)
        return villes

    def get_ville_by_zone_and_corps(self,zone,corps):
        myquery = { "zone": zone, "corps": corps }
        villes = self.villes.find(myquery)
        toreturns = []
        for ville in villes:
            ville['_id'] = str(ville['_id'])
            toreturns.append(ville)
        return jsonify(toreturns)

    def create_new_ville(self,jsn):
        # Create index on code of ville field to prevent duplicated inserting
        # self.villes.create_index([('code_numerique_ville', '')], unique=True)
        try:
            self.villes.insert(jsn)
            return True
        except DuplicateKeyError:
            return False


    def update_ville(self,id,newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        if self.villes.update_one(query,updated):
            return True
        else:
            return False

    def delete_ville(self, id):
        query = {"_id": ObjectId(id)}
        if self.villes.delete_one(query):
            return True
        else:
            return False

    def delete_ville_by_code(self, code_ville):
        query = {"code_ville": code_ville}
        if self.villes.remove(query):
            return True
        else:
            return False




