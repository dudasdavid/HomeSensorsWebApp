import sys
from os.path import dirname, exists, join

DATA_DIR = join(dirname(__file__), 'data')

DBS = ['home_sensors_v1']

def on_server_loaded(server_context):
    if not all(exists(join(DATA_DIR, '%s.csv' % x)) for x in DBS):
        print()
        print("Due to performance considerations, you must first run background_downloader.py to download the data set yourself.")
        print()

        sys.exit(1)