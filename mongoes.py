from pymongo import MongoClient
from datetime import datetime
from elasticsearch import Elasticsearch

client = MongoClient()
db = client['pymongotest']

posts = db.posts
post_data = {
	'title' : "Python and Mngodb",
	'content' : 'Pymingi si fun',
	'author' : 'Bill',
	'pubdate' : datetime.utcnow()
}

result = posts.insert_one(post_data)
print('One post: {0}'.format(result.inserted_id))

bills_post = posts.find_one({'author': 'Bill'})
print(bills_post)

getpost = posts.find_one({'author': 'Scott'})
print(getpost)

bills_post.pop('_id', None)

es = Elasticsearch()
es.index(index='posts', doc_type='blog', id=1, body=bills_post)

print("Now querying elasticsearch")
res = es.search(index='posts', doc_type='blog', body={"query": {"match": {"author": "Bill"}}})
print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
    print("%s) %s" % (doc['_id'], doc['_source']['content']))