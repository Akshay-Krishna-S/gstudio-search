from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
print("f")
db = client['tutorial']
coll = db['articles']

doc = {
	"title": "An article about MongoDB and Python",
	"author": "Loda",
	"publication_date": datetime.utcnow()
}

doc_id = coll.insert_one(doc).inserted_id
print (doc_id)

my_doc = coll.find_one({'_id':doc_id})
print (my_doc)