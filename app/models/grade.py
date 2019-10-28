from pymongo import MongoClient
from flask import jsonify, session
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class Grade():
    client = MongoClient("localhost", 27017)
    db = client["missions"]
    grades = db["grades"]

    def get_grades(self):
        result = self.grades.find()
        toreturns = []
        # return [str(grade['_id']) for grade in result]

        return result
        # for grade in result:
        #     grade['_id'] = str(grade['_id'])
        #     toreturns.append(grade)
        # return jsonify(toreturns)

    def get_all_codes_of_grades(self):
        result = self.grades.find()
        toreturns = []
        for grade in result:
            toreturns.append(grade['code_grade'])
        return toreturns

    def get_grade(self, grade_id):
        myquery = {"_id": ObjectId(grade_id)}
        return self.grades.find_one(myquery)


    def get_grade_by_code(self, code_grade):
        myquery = {"code_grade": code_grade}
        grades = self.grades.find(myquery)
        return grades

    def get_grade_by_zone_and_corps(self, zone, corps):
        myquery = {"zone": zone, "corps": corps}
        grades = self.grades.find(myquery)
        toreturns = []
        for grade in grades:
            grade['_id'] = str(grade['_id'])
            toreturns.append(grade)
        return jsonify(toreturns)

    def create_new_grade(self, jsn):
        # Create index on code of grade field to prevent duplicated inserting
        self.grades.create_index([('libelle_grade', '')], unique=True)
        try:
            self.grades.insert(jsn)
            return True
        except DuplicateKeyError:
            return False

    def update_grade(self, id, newvalues):
        query = {"_id": ObjectId(id)}
        updated = {"$set": newvalues}
        if self.grades.update_one(query, updated):
            return True
        else:
            return False

    def delete_grade(self, id):
        query = {"_id": ObjectId(id)}
        if self.grades.delete_one(query):
            return True
        else:
            return False

    def delete_grade_by_code(self, code_grade):
        query = {"code_grade": code_grade}
        if self.grades.remove(query):
            return True
        else:
            return False
