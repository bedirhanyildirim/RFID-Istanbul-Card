## Google Sheets Libs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
## RFID Module Lib
from pirc522 import RFID
rdr = RFID()

## Google Cloud Sheet Connection
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
client =  gspread.authorize(creds)
sheet = client.open("rfid-akbil").sheet1

## Find UID in Google Sheets
def findUID(uid):
    print("Card id is: ", uid)
    findRow = sheet.find(uid).row
    findCol = sheet.find(uid).col
    getBakiye = int(sheet.cell(findRow, findCol+1).value)
    if getBakiye == 0:
        print("Insufficient balance!")
    else:
        sheet.update_cell(findRow, findCol+1, getBakiye-2)
        print("Current balance is: ", int(sheet.cell(findRow, findCol+1).value), "TL")

## Infinite loop for reading
while True:
    rdr.wait_for_tag()
    (error, tag_type) = rdr.request()
    if not error:
        (error, uid) = rdr.anticoll()
        if not error:
            newData = str(uid)
            if (len(newData) > 10) and (newData[:1] == "[") and (newData[-1] == "]"):
                print("UID: " + newData)
                findUID(newData)
			
rdr.cleanup()
