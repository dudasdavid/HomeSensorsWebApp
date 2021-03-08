import firebase_admin
from firebase_admin import credentials, firestore

from SimpleLogger import SimpleLogger

logger = SimpleLogger(verbose = True, loggerName = f"Background downloader")

logger.log(f"Connecting to Firestore.")
cred = credentials.Certificate("home-sensors-credentials.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()
collection = firestore_db.collection('home_sensors_v1')

# Checking the latest sample in Firestore
logger.log(f"Check the latest sample in Firestore.")
try:
    result = collection.order_by('date',direction='DESCENDING').limit(1).get()
    firestore_latest = result[0].to_dict()['timestamp']
    logger.log(f"Latest data timestamp in Firestore: {firestore_latest}")
except Exception as e:
    logger.log(f"Error during downloading data from Firebase: {e}", messageType = "ERROR")
    exit()

# Checking the latest sample in local database
file_name = "data/home_sensors_v1.csv"
logger.log(f"Checking the latest sample in local database.")
try:
    fh = open(file_name, 'r')
    local_data = fh.readlines()
    local_latest = local_data[-1].split(",")[0]
    logger.log(f"Latest data timestamp in `{file_name}` local csv: {local_latest}")
    fh.close()
except FileNotFoundError:
    logger.log(f"Local database `{file_name}` doesn't exist.", messageType = "WARN")
    local_latest = None

if firestore_latest == local_latest:
    logger.log("You have the latest database, nothing to do.", messageType = "OK")
    exit()
elif local_latest == None:
    logger.log("There is no local database, downloading everything from Firestore.", messageType = "WARN")

    results = collection.order_by('date',direction='ASCENDING').get() # another way - get the last document by date

    logger.log(f"Writing data to `{file_name}`.")
    # csv example: 19980102,0,3.31397,3.95098,3.28236,3.95098,24947201.1
    fh = open(file_name, 'w')

    for item in results:
        #print(item.to_dict())
        fh.write(f"{item.to_dict()['timestamp']},{item.to_dict()['kitchen_temp']},{item.to_dict()['kitchen_hum']},{item.to_dict()['kitchen_bat']}," \
                f"{item.to_dict()['outside_temp']},{item.to_dict()['outside_hum']},{item.to_dict()['outside_bat']}," \
                f"{item.to_dict()['filament_temp']},{item.to_dict()['filament_hum']},{item.to_dict()['filament_bat']}," \
                f"{item.to_dict()['bathroom_temp']},{item.to_dict()['bathroom_hum']},{item.to_dict()['bathroom_bat']}\n")

    fh.close()
    logger.log(f"Local databased was created.")
else:
    logger.log(f"Local latest timestamp is {local_latest}, Firestore latest timestamp is {firestore_latest}, incremental update needed!", messageType = "WARN")
    
    logger.log(f"Appending data to `{file_name}`.")
    fh = open(file_name, 'a')
    
    # Try querying only 5 samples
    querySize = 5
    logger.log(f"Querying {querySize} items from Firestore.")
    results = collection.order_by('date',direction='DESCENDING').limit(querySize).get()
    results.reverse()
    startFlag = False
    for i, item in enumerate(results):
        #print(i, item.to_dict()['timestamp'], startFlag)
        if startFlag:
            fh.write(f"{item.to_dict()['timestamp']},{item.to_dict()['kitchen_temp']},{item.to_dict()['kitchen_hum']},{item.to_dict()['kitchen_bat']}," \
                    f"{item.to_dict()['outside_temp']},{item.to_dict()['outside_hum']},{item.to_dict()['outside_bat']}," \
                    f"{item.to_dict()['filament_temp']},{item.to_dict()['filament_hum']},{item.to_dict()['filament_bat']}," \
                    f"{item.to_dict()['bathroom_temp']},{item.to_dict()['bathroom_hum']},{item.to_dict()['bathroom_bat']}\n")
        
        if local_latest == item.to_dict()['timestamp']:
            startFlag = True

    if startFlag:
        logger.log(f"Local database was successfully updated from the last {querySize} samples.", messageType = "OK")
        fh.close()
        exit()

    # Only go through at this point if update was unsuccesful.
    oldQuerySize = querySize
    querySize = 20
    logger.log(f"{oldQuerySize} samples were not enough, trying with {querySize}!", messageType = "WARN")

    # Try querying 20 samples
    logger.log(f"Querying {querySize} items from Firestore.")
    results = collection.order_by('date',direction='DESCENDING').limit(querySize).get()
    results.reverse()
    startFlag = False
    for i, item in enumerate(results):
        #print(i, item.to_dict()['timestamp'], startFlag)
        if startFlag:
            fh.write(f"{item.to_dict()['timestamp']},{item.to_dict()['kitchen_temp']},{item.to_dict()['kitchen_hum']},{item.to_dict()['kitchen_bat']}," \
                    f"{item.to_dict()['outside_temp']},{item.to_dict()['outside_hum']},{item.to_dict()['outside_bat']}," \
                    f"{item.to_dict()['filament_temp']},{item.to_dict()['filament_hum']},{item.to_dict()['filament_bat']}," \
                    f"{item.to_dict()['bathroom_temp']},{item.to_dict()['bathroom_hum']},{item.to_dict()['bathroom_bat']}\n")
        
        if local_latest == item.to_dict()['timestamp']:
            startFlag = True

    if startFlag:
        logger.log(f"Local database was successfully updated from the last {querySize} samples.", messageType = "OK")
        fh.close()
        exit()    

    # Only go through at this point if update was unsuccesful.
    oldQuerySize = querySize
    querySize = 100
    logger.log(f"{oldQuerySize} samples were not enough, trying with {querySize}!", messageType = "WARN")

    # Try querying 20 samples
    logger.log(f"Querying {querySize} items from Firestore.")
    results = collection.order_by('date',direction='DESCENDING').limit(querySize).get()
    results.reverse()
    startFlag = False
    for i, item in enumerate(results):
        #print(i, item.to_dict()['timestamp'], startFlag)
        if startFlag:
            fh.write(f"{item.to_dict()['timestamp']},{item.to_dict()['kitchen_temp']},{item.to_dict()['kitchen_hum']},{item.to_dict()['kitchen_bat']}," \
                    f"{item.to_dict()['outside_temp']},{item.to_dict()['outside_hum']},{item.to_dict()['outside_bat']}," \
                    f"{item.to_dict()['filament_temp']},{item.to_dict()['filament_hum']},{item.to_dict()['filament_bat']}," \
                    f"{item.to_dict()['bathroom_temp']},{item.to_dict()['bathroom_hum']},{item.to_dict()['bathroom_bat']}\n")
        
        if local_latest == item.to_dict()['timestamp']:
            startFlag = True

    if startFlag:
        logger.log(f"Local database was successfully updated from the last {querySize} samples.", messageType = "OK")
        fh.close()
        exit()

    # Only go through at this point if update was unsuccesful.
    oldQuerySize = querySize
    querySize = 1000
    logger.log(f"{oldQuerySize} samples were not enough, trying with {querySize}!", messageType = "WARN")

    # Try querying 20 samples
    logger.log(f"Querying {querySize} items from Firestore.")
    results = collection.order_by('date',direction='DESCENDING').limit(querySize).get()
    results.reverse()
    startFlag = False
    for i, item in enumerate(results):
        #print(i, item.to_dict()['timestamp'], startFlag)
        if startFlag:
            fh.write(f"{item.to_dict()['timestamp']},{item.to_dict()['kitchen_temp']},{item.to_dict()['kitchen_hum']},{item.to_dict()['kitchen_bat']}," \
                    f"{item.to_dict()['outside_temp']},{item.to_dict()['outside_hum']},{item.to_dict()['outside_bat']}," \
                    f"{item.to_dict()['filament_temp']},{item.to_dict()['filament_hum']},{item.to_dict()['filament_bat']}," \
                    f"{item.to_dict()['bathroom_temp']},{item.to_dict()['bathroom_hum']},{item.to_dict()['bathroom_bat']}\n")
        
        if local_latest == item.to_dict()['timestamp']:
            startFlag = True

    if startFlag:
        logger.log(f"Local database was successfully updated from the last {querySize} samples.", messageType = "OK")
        fh.close()
        exit()

    # Only go through at this point if update was unsuccesful.
    logger.log(f"{querySize} samples were not enough, exiting with ERROR!", messageType = "ERROR")
    fh.close()
    exit()