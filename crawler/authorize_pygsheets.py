import os
import pygsheets

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
CREDENTIAL_DIR = os.path.join(CURRENT_PATH, "confidential")
CREDENTIAL_PATH = os.path.join(CREDENTIAL_DIR, "client_secret.json")
try:
    gc = pygsheets.authorize(client_secret=CREDENTIAL_PATH)
except Exception as e:
    print(f"[ WARNING ] - Error while authenticate: {e}")