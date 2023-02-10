#!flask/bin/python

from flask import Flask
from flask_restful import Resource, Api, reqparse, fields
from pymongo import MongoClient
from bson.objectid import ObjectId
import bson.json_util as json_util
import json

serverApp = Flask(__name__)
api = Api(serverApp)

# database credentials included in code here for simplicity/convenience, I wouldn't do this in production ;)
DBHOST = "mongodb+srv://powerflex:RAXBLdx8@sprocketfactory.oyrxhjv.mongodb.net/?retryWrites=true&w=majority"

class SprocketAPI(Resource):
    """
    Parent class with shared database connection methods.
    """
    def getSprocketCollection(self):
        """fetch sprocket collection from mongo"""

        client = MongoClient(DBHOST)
        sprocketdb = client['powerflexdb']
        return sprocketdb['sprockets']

    def getFactoryCollection(self):
        """fetch factory collection from mongo"""

        client = MongoClient(DBHOST)
        factorydb = client['powerflexdb']
        return factorydb['factories']

class SprocketGet(SprocketAPI):
    def get(self, id):
        sprockets = self.getSprocketCollection()
        cursor = sprockets.find({"_id" : ObjectId(id)})
        return json_util.dumps(cursor[0])

class SprocketPut(SprocketAPI):
    def __init__(self):
        #define the arguments we can be passed for sprocket modification
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('teeth', type = int, required = False, location = 'json')
        self.reqparse.add_argument('pitch_diameter', type = float, required = False, location = 'json')
        self.reqparse.add_argument('outside_diameter', type = float, required = False, location = 'json')
        self.reqparse.add_argument('pitch', type = float, required = False, location = 'json')
        super(SprocketPut, self).__init__()

    def put(self,id):
        sprockets = self.getSprocketCollection()
        args = self.reqparse.parse_args()
        for a in args:
            if args[a] is not None:
                result = sprockets.update_one(
                    {"_id" : ObjectId(id)},
                    {"$set" : {a : args[a]} }
                )

class SprocketPost(SprocketAPI):
    def __init__(self):
        #define the arguments we must be passed for sprocket creation
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('teeth', type = int, required = True, location = 'json')
        self.reqparse.add_argument('pitch_diameter', type = float, required = True, location = 'json')
        self.reqparse.add_argument('outside_diameter', type = float, required = True, location = 'json')
        self.reqparse.add_argument('pitch', type = float, required = True, location = 'json')
        super(SprocketPost, self).__init__()

    def post(self):
        sprockets = self.getSprocketCollection()
        args = self.reqparse.parse_args()
        result = sprockets.insert_one(
            {
                'teeth' : args['teeth'],
                'pitch_diameter' : args['pitch_diameter'],
                'outside_diameter' : args['outside_diameter'],
                'pitch' : args['pitch']
            }
        )
        print("Added new sprocket with id: " + str(result.inserted_id))
        


class FactoryDataGetAll(SprocketAPI):
    def get(self):
        cursor = self.getFactoryCollection().find({})
        return json_util.dumps(cursor)

class FactoryDataGet(SprocketAPI):
    def get(self, id):
        factories = self.getFactoryCollection()
        cursor = factories.find({"_id" : ObjectId(id)})
        return json_util.dumps(cursor[0])


# register endpoints
api.add_resource(SprocketGet, '/powerflex/api/sprocket/<string:id>', endpoint = 'sprocket')
api.add_resource(SprocketPut, '/powerflex/api/updatesprocket/<string:id>', endpoint = 'updatesprocket')
api.add_resource(SprocketPost, '/powerflex/api/newsprocket', endpoint = 'newsprocket')
api.add_resource(FactoryDataGetAll, '/powerflex/api/factorydata', endpoint = 'allfactorydata')
api.add_resource(FactoryDataGet, '/powerflex/api/factorydata/<string:id>', endpoint = 'factorydata')


sprocket_fields = {
    'teeth': fields.Integer,
    'pitch_diameter': fields.Float,
    'outside_diameter': fields.Float,
    'pitch': fields.Float,
}

if __name__ == '__main__':
    serverApp.run(debug=True)


