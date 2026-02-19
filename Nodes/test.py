from database import collection

print("Connected!")
print(collection.count_documents({}))
