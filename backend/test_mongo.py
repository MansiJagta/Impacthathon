from app.database.mongo import policies_collection

p = policies_collection.find_one({"policyNumber": "MOT-12345678"})
print(p)