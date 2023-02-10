from unittest import TestCase
import subprocess
from seed_ingest import populate, getFactoryIDs, getSprocketIDs

"""
RUNNING THESE TESTS WILL RESET THE DATA IN THE PERSISTENT DATASTORE TO THE SEED VALUES
Persisted ObjectIDs will also change with every populate()
"""

class TestPopulate(TestCase):
    populate()
    firstSprocket = str(getSprocketIDs()[0])
    shellcmd = 'curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/' + firstSprocket + '"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    #check that the first sprocket has 5 teeth (all the seed sprockets do)
    assert output[64] == '5'

class TestGetAllFactoryData(TestCase):
    populate()
    output = subprocess.check_output('curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/factorydata"', shell=True).decode("utf-8")
    # check that all factory ids are present in output
    for id in getFactoryIDs():
        assert (str(id) in output)

class TestGetSingleFactoryData(TestCase):
    populate()
    firstFactory = str(getFactoryIDs()[0])
    output = subprocess.check_output('curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/factorydata/' + firstFactory + '"', shell=True).decode("utf-8")
    # match the last timestamp of the first factory
    assert output[-15:-6] == '611195958'

class TestSprocketLookup(TestCase):
    populate()
    middleSprocket = str(getSprocketIDs()[1])
    shellcmd = 'curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/' + middleSprocket + '"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    assert output[64] == '5'

class TestInvalidSprocketLookup(TestCase):
    populate()
    middleSprocket = str(getSprocketIDs()[1])
    output = subprocess.check_output('curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/63e5643bbe5eb8e7e89a445b"', shell=True).decode("utf-8")
    # we should get an index error when we ask for a sprocket that doesn't exist
    assert 'IndexError' in output

class TestSprocketUpdate(TestCase):
    populate()
    lastSprocket=str(getSprocketIDs()[2])
    # change one of the sprockets to have a lot of teeth
    shellcmd = 'curl -X PUT -H "Content-type: application/json" -d "{\\"teeth\\" : 6626}" "localhost:5000/powerflex/api/updatesprocket/' + lastSprocket + '"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    shellcmd = 'curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/' + lastSprocket + '"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    assert '6626' in output
    lastSprocketAgain = str(getSprocketIDs()[2])
    assert lastSprocket == lastSprocketAgain # id should not have changed

class TestSprocketAdd(TestCase):
    populate()
    shellcmd = 'curl -X POST -H "Content-type: application/json" -d "{\\"teeth\\" : 10, \\"pitch_diameter\\" : 4.5, \\"outside_diameter\\" : 3.9, \\"pitch\\" : 3.14}" "localhost:5000/powerflex/api/newsprocket"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    newSprockID = str(getSprocketIDs()[3])
    shellcmd = 'curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/' + newSprockID + '"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    # check that the new sprocket has 10 teeth like we told it to. 
    assert output[64:66] == '10'

class TestSprocketCreationExtraArgs(TestCase):
    populate()
    #try creating a sprocket with some random extra args
    shellcmd = 'curl -X POST -H "Content-type: application/json" -d "{\\"teeth\\" : 11, \\"weight_on_the_moon\\" : 10, \\"twitter_handle\\" : 10, \\"pitch_diameter\\" : 4.5, \\"outside_diameter\\" : 3.9, \\"pitch\\" : 3.14}" "localhost:5000/powerflex/api/newsprocket"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    newSprockID = str(getSprocketIDs()[3])
    shellcmd = 'curl -X GET -H "Content-type: application/json" "localhost:5000/powerflex/api/sprocket/' + newSprockID + '"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    # check that the new sprocket has 11 teeth and was created in spite of extra args
    assert output[64:66] == '11'

class TestSprocketCreationMissingArgs(TestCase):
    populate()
    #make sure we get an error if we leave out required args when creating sprockets
    shellcmd = 'curl -X POST -H "Content-type: application/json" -d "{\\"pitch_diameter\\" : 4.5, \\"outside_diameter\\" : 3.9, \\"pitch\\" : 3.14}" "localhost:5000/powerflex/api/newsprocket"'
    output = subprocess.check_output(shellcmd, shell=True).decode("utf-8")
    assert 'Missing required parameter' in output
