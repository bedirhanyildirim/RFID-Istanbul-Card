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

## Last read card uid
data = ""

## Find UID in Google Sheets
def findUID (uid):
    try:
        print("Card id is: ", uid)
        findRow = sheet.find(uid).row
        findCol = sheet.find(uid).col
        getBakiye = int(sheet.cell(findRow, findCol+1).value)
        print("Current balance is: ", getBakiye, "TL")
        addBakiye = int(input("How much would you cant to add: "))
        sheet.update_cell(findRow, findCol+1, getBakiye+addBakiye)
        print(uid, " card balance was updated to ", sheet.cell(findRow, findCol+1).value, "TL")
    except:
        print("New rfid card find.")
        addBakiye = int(input("How much would you cant to add: "))
        insertRow = [uid, addBakiye]
        sheet.insert_row(insertRow, 2)
        print("Card added.")

## Infinite loop for reading
while True:
	rdr.wait_for_tag()
	(error, tag_type) = rdr.request()
	if not error:
		(error, uid) = rdr.anticoll()
		if not error:
			newData = str(uid)
			if (len(newData) > 10) and (newData[:1] == "[") and (newData[-1] == "]"):
				if (data != newData):
					print("UID: " + newData)
					data = newData
					findUID(data)
			
rdr.cleanup()
