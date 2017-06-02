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
		document = json.load(fp)
	
	document["id"] = document.pop("_id")
	document["type"] = document.pop("_type")
	if("object_value" in document.keys()):
		document["object_value"] = str(document["object_value"])	

	print("now indexing")
	es.index(index='gstudio', doc_type='generic', id=document["id"]["$oid"], body=json.dumps(document))
	print("indexed document %d" % k)

def main():
	print("Starting the indexing process")

	dir = '/home/dvjsm/Gstudio/data/rcs-repo/'
	index_directory(dir)

main()