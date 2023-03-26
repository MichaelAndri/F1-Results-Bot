import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytesseract
from PIL import Image

# set up credentials to access Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# get image URL and download image
img_url = input("Enter image URL: ")
img_data = requests.get(img_url).content

# perform OCR with Tesseract OCR library
img = Image.open(io.BytesIO(img_data))
text = pytesseract.image_to_string(img)

print(text)

# parse text to extract driver names and finishing positions
driver_positions = []
for line in text.split('\n'):
    if line.isnumeric():
        driver_positions.append(int(line))

# calculate points for each driver
points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
driver_points = [points[i-1] if i <= 10 else 0 for i in driver_positions]
print(driver_points)

# open Google Sheets and update F1 Results sheet with driver points
sheet = client.open('F1 Results').sheet1
driver_names = sheet.col_values(1)[1:]
for i in range(len(driver_names)):
    if driver_names[i].upper() not in ['DNF', 'DSQ']:
        sheet.update_cell(i+2, 2, driver_points[i])