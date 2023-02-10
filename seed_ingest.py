# Run this script to populate the cloud-based mongodb datastore with the seed data.
# Mongodb assigns 24 character hex strings as ids, and these are returned and 
# printed for convenience. Also includes helper functions for getting the current
# ObjectIDs from the datastore. 



import json, pymongo

DBHOST = "mongodb+srv://powerflex:RAXBLdx8@sprocketfactory.oyrxhjv.mongodb.net/?retryWrites=true&w=majority"

def populate():
    client = pymongo.MongoClient(DBHOST)
    sprocketdb = client['powerflexdb']
    sprocket_collection = sprocketdb["sprockets"]
    factory_collection = sprocketdb["factories"]

    # purge any persisted data in these two collections
    sprocket_collection.delete_many({})
    factory_collection.delete_many({})

    # ingest seed data
    with open('seed_sprocket_types.json') as sprocketjson:
        sprockets_seed = json.load(sprocketjson)
    sprocket_collection.insert_many(sprockets_seed['sprockets'])

    with open('seed_factory_data.json') as factoryjson:
        factories_seed = json.load(factoryjson)
    factory_collection.insert_many(factories_seed['factories'])

    # list ids assigned to ingested data

    sprox = sprocket_collection.find({})
    id_list = 'Sprockets:\n'
    for s in sprox:
        id_list = id_list + str(s['_id'])+'\n'

    facts = factory_collection.find({})
    id_list += '\nFactories:\n'
    for f in facts:
        id_list = id_list + str(f['_id'])+'\n'

    if __name__ == '__main__': print(id_list)

def getSprocketIDs():
    """returns a list of bson formatted ObjectIDs for sprockets currently in the datastore"""
    sprocketIDs = []
    client = pymongo.MongoClient(DBHOST)
    sprocketdb = client['powerflexdb']
    sprocket_collection = sprocketdb["sprockets"]
    allsprox = sprocket_collection.find({})
    for s in allsprox:
        sprocketIDs.append(s['_id'])
    return sprocketIDs

def getFactoryIDs():
    """returns a list of bson formatted ObjectIDs for factories currently in the datastore"""
    factoryIDs = []
    client = pymongo.MongoClient(DBHOST)
    factdb = client['powerflexdb']
    factory_collection = factdb["factories"]
    allfacts = factory_collection.find({})
    for s in allfacts:
        factoryIDs.append(s['_id'])
    return factoryIDs

if __name__ == '__main__':
    populate()