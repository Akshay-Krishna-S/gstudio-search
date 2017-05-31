from elasticsearch import Elasticsearch
import os
import sys
import json

es = Elasticsearch(timeout=300)

def index_directory(dir):
	k = 1
	for path, dirs, files in os.walk(dir):
		for file in files:
			fname = os.path.join(path,file)
			ext = (fname.rsplit('.',1))[1]
			if(ext=='json'):
				index_file(fname,k)
				k+=1

def index_file(fname,k):
	with open(fname, 'r') as fp:
		docstr = fp.read()
		#docstr = docstr.replace("\\n", " ")
		#docstr = docstr.replace("\\r", "")
		document = json.loads(docstr)
	
	document["id"] = document.pop("_id")
	document["type"] = document.pop("_type")
	if("object_value" in document.keys()):
		document["object_value"] = str(document["object_value"])	

	# if(k>=13):
	# 	print(json.dumps(document))
	print("now indexing")
	es.index(index='gstudio', doc_type='generic', id=document["id"]["$oid"], body=json.dumps(document))
	print("indexed document %d" % k)

def main():
	print("creating object")

	dir = '/home/dvjsm/Gstudio/data/rcs-repo/'
	index_directory(dir)

	# res = es.search(index='posts', doc_type='blog', body={"query": {"match": {"author": "Bill"}}})
	# print("%d documents found" % res['hits']['total'])
	# for doc in res['hits']['hits']:
	#     print("%s) %s" % (doc['_id'], doc['_source']['content'])
main()