from elasticsearch import Elasticsearch
import os
import sys
import json

es = Elasticsearch("http://elsearch:changeit@localhost:9200")
reload(sys)
sys.setdefaultencoding('utf8')


all_map = {}
author_map = {}
group_map = {}
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
		try:
			document = json.load(fp)
		except:
			#print("doc is empty")
			return
		# else:
			#print(fname)

	document["id"] = document.pop("_id",None)
	document["type"] = document.pop("_type",None)
	print(document["type"])
	#print("now mapping")
	create_map(document)
	#print("mapped %d" % k)



def create_map(document):
	if "name" in document.keys():
		all_map[document["id"]["$oid"]]=document["name"]
		if document["type"]=="Author":
			ids=[]
			ids.append(document["id"]["$oid"])
			ids.append(document["name"])
			author_map[document["created_by"]] = ids
		if document["type"]=="Group":
			group_map[document["id"]["$oid"]]=document["name"]




def main():
	dir = '/home/nazgul/Ashwin/data/rcs-repo/'
	index_directory(dir)

	# f = open("all_mappings.txt","a")
	# for i in all_map.keys():
	# 	strs=i+" "+all_map[i]+"\n"
	# 	f.write(strs)
	# f.close()
	f = open("author_mappings.txt","a")
	for i in author_map.keys():
		print(i)
		print(author_map[i])
		strs=str(i)+" "+author_map[i][0]+" "+author_map[i][1]+"\n"
		f.write(strs)
	f.close()
	# f = open("group_mappings.txt","a")
	# for i in group_map.keys():
	# 	strs=i+" "+group_map[i]+"\n"
	# 	f.write(strs)
	# f.close()



main()
