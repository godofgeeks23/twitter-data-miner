# from oauth2client.service_account import ServiceAccountCredentials
# import gspread
# import json

# scopes = [
# 'https://www.googleapis.com/auth/spreadsheets',
# 'https://www.googleapis.com/auth/drive'
# ]
# credentials = ServiceAccountCredentials.from_json_keyfile_name("verified-security-sources-6b7e7530d6f5.json", scopes) #access the json key you downloaded earlier 
# file = gspread.authorize(credentials) # authenticate the JSON key with gspread
# sheet = file.open("Python_MUO_Google_Sheet")  #open sheet
# sheet = sheet.sheet_name  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1


import pygsheets
import pandas as pd
gc = pygsheets.authorize(service_file='verified-security-sources-6b7e7530d6f5.json') # provide the json_file name including the .json extension
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1ELBSsc5tQIjZFHCmTofbwflOx37CK0OOpXEiMa2Irto/edit?usp=sharing")

print(sh.id) #to get the id of the spreadsheet.
print(sh.worksheets())#to get a list of all worksheets.
