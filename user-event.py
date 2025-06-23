import pymongo
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Set up Google Sheets API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from your JSON file (replace with your actual filename)
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "your_credentials_file.json", scope
)
client = gspread.authorize(creds)

# Connect to your MongoDB database (update with your actual connection string)
mongo_client = pymongo.MongoClient("mongodb://...")

# Select your database and collection
db = mongo_client["your_database_name"]
collection = db["your_collection_name"]

# Fetch data from MongoDB
data = list(collection.find({}))
df = pd.DataFrame(data)

# Format specific columns
# if "_id" in df.columns:
#     df["_id"] = df["_id"].astype(str)

# if "created_at" in df.columns:
#     df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime('%Y-%m-%d %H:%M:%S')

# Open your Google Sheet (replace with your actual sheet name)
sheet = client.open("Your Google Sheet Name").sheet1
sheet.clear()  # Clears old data

# Clean invalid values (optional)
# df = df.replace([float('inf'), float('-inf')], None)
# df = df.where(pd.notnull(df), None)
# df = df.applymap(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

# Upload data to Google Sheet
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Data synced successfully with Google Sheets!")
