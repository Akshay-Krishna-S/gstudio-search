from elasticsearch import Elasticsearch
import os
import sys
import json

es = Elasticsearch("http://elsearch:changeit@localhost:9200")

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


	if document["type"]=="GSystem":
		if document["if_file"]["mime_type"] is not None:
			data = document["if_file"]["mime_type"].split("/")
			print("now indexing")
			es.index(index='gstudio', doc_type=data[0], id=document["id"]["$oid"], body=json.dumps(document))
			print("indexed document %d" % k)
		else:
			data = "NotMedia"
			print("now indexing")
			es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
			print("indexed document %d" % k)
	elif document["type"]=="Author":
		data = "Author"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="GAttribute":
		data = "GAttribute"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="GRelation":
		data = "GRelation"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="AttributeType":
		data = "AttributeType"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="Counter":
		data = "Counter"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="Filehive":
		data = "Filehive"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="RelationType":
		data = "RelationType"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	elif document["type"]=="Group":
		data = "Group"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)
	else:
		data = "DontCare"
		print("now indexing")
		es.index(index='gstudio', doc_type=data, id=document["id"]["$oid"], body=json.dumps(document))
		print("indexed document %d" % k)



def main():
	print("Starting the indexing process")

	dir = '/home/nazgul/Ashwin/data/rcs-repo/'
	index_directory(dir)

main()
