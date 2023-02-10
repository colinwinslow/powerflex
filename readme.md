# Powerflex Rest API Take-home interview assignment

This python application provides a simple RESTful interface to the provided sprocket and sprocket factory data. It uses a free instance in the MongoDB Atlas cloud for a datastore, so an internet connection is required.

Unit tests are included which use curl to exercise HTTP methods on server application running locally. I developed and tested these using the Windows Subsystem for Linux, and they *should* work on OSX or Linux, but probably not on a plain Windows machine. You will need Python 3.6+, and may need to ```pip install``` ```flask```, ```flask-restful```, and ```pymongo```. 

## Loading the Seed Data into mongodb:
Open a terminal window, navigate to the directory containing seed_ingest.py, and run ```python3 seed_ingest.py```.
This will read the supplied json files from the same directory and upload the data into the mongodb Atlas cloud. The ObjectIDs are created on the fly by Mongo and will be printed in the terminal window when you run seed_ingest.py. You may want to copy some of these for testing.

## Starting the Server:
Open a terminal window (or use the same one from the previous step), navigate to the directory containing sprocketFactoryServer.py and run ```python3 sprocketFactoryServer.py```

## Using the server:
Once the server is running you can interact with it in several ways. The simplest way is through a web browser, which will allow you to access the API's GET methods. Open a web browser and go to ```localhost:5000/powerflex/api/sprocket/<sprocket id>```, pasting in one of the sprocket identifiers that was printed when you ran seed_ingest.py. Similarly, you can go to ```localhost:5000/powerflex/api/factorydata``` to see all factory data, or ```/powerflex/api/factorydata/<factory id>``` to view a specific factory. 

When modifying sprockets, you can update any number of the fields in a single request. The teeth field must be an integer, and 'id' must be a 24 character hexadecimal string. Pitch, pitch_diameter, and outside_diameter are floats. 

When creating sprockets, you must supply all four fields.

To access the API endpoints that involve changing data, you will need to use curl or a similar tool that can encapsulate json data in HTTP requests. The included unit tests in test.py do this. Be aware that each testcase purges the database and reloads it from the seed data, so running the tests will clear anything you might have persisted. 


## Sample curl commands
read factory data
```curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/factorydata"```

read specific factory data
```curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/factorydata/<factory id>"```

read specific sprocket data
```curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/<sprocket id>"```

modify a sprocket to have one million teeth
```curl -X PUT -H "Content-type: application/json" -d "{\"teeth\" : 1000000}" "localhost:5000/powerflex/api/updatesprocket/<sprocket id>"```

modify multiple sprocket fields
```curl -X PUT -H "Content-type: application/json" -d "{\"teeth\" : 10, \"pitch\" : 45.01}" "localhost:5000/powerflex/api/updatesprocket/<sprocket id>"```

create a new sprocket
```curl -X POST -H "Content-type: application/json" -d "{\"teeth\" : 10, \"pitch_diameter\" : 4.5, \"outside_diameter\" : 3.9, \"pitch\" : 3.14}" "localhost:5000/powerflex/api/newsprocket"```


Thank you for considering me for this position!

Colin Winslow 
colinwinslow@gmail.com
520.780.0061
