from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://manubhute02_db_user:manasvi123@cluster0.z5921d6.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=False,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
)

db = client["claims_db"]

historical_claims = db["historical_claims"]
live_claims = db["live_claims"]
reviewer_queue = db["reviewer_queue"]
