import pymongo
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheets API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# ملف JSON اللي حملتيه من Google Cloud
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "cogent-tree-463812-h9-856209138fce.json", scope
)
client = gspread.authorize(creds)

# الاتصال بقاعدة MongoDB
mongo_client = pymongo.MongoClient("mongodb://root:example@localhost:27017/admin")
print(mongo_client.list_database_names())
db = mongo_client["nota-nota-20230828"]  # اسم قاعدة البيانات
collection = db["event_user"]            # اسم الكوليكشن

# جلب البيانات
data = list(collection.find({}))
df = pd.DataFrame(data)

# معالجة الأعمدة
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime('%Y-%m-%d %H:%M:%S')

# فتح Google Sheet (لازم يكون اسمه "Event User Data")
sheet = client.open("Event User Data").sheet1
sheet.clear()

# تنظيف القيم الغير صالحة
df = df.replace([float('inf'), float('-inf')], None)
df = df.where(pd.notnull(df), None)
df = df.applymap(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

# تحديث البيانات مع الأعمدة
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ تمت مزامنة البيانات مع Google Sheets بنجاح!")

