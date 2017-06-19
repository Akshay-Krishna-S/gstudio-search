from elasticsearch import Elasticsearch
import os
import sys
import json

es = Elasticsearch("http://elsearch:changeit@localhost:9200")
index_type = ""

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
			print("doc is empty")
			return
		else:
			print(fname)

	document["id"] = document.pop("_id")
	document["type"] = document.pop("_type")
	if("object_value" in document.keys()):
		document["object_value"] = str(document["object_value"])	#for consistent mapping 

	print("now indexing")
	if document["type"]=="GSystem":
		if('if_file' in document.keys()):
			if document["if_file"]["mime_type"] is not None:
				data = document["if_file"]["mime_type"].split("/")
				index_type = data[0]
			else:
				index_type = "NotMedia"
		else:
			index_type = "NotMedia"
		#index_type = "GSystem"			
	elif document["type"]=="Author":
		index_type = "Author"
	elif document["type"]=="GAttribute":
		index_type = "GAttribute"
	elif document["type"]=="GRelation":
		index_type = "GRelation"
	elif document["type"]=="AttributeType":
		index_type = "AttributeType"
	elif document["type"]=="Filehive":
		index_type = "Filehive"
	elif document["type"]=="RelationType":
		index_type = "RelationType"
	elif document["type"]=="Group":
		index_type = "Group"
	else:
		index_type = "DontCare"

	es.index(index='nroer_pro', doc_type=index_type, id=document["id"]["$oid"], body=json.dumps(document))
	print("indexed document %d" % k)

def main():
	print("Starting the indexing process")

	if(es.indices.exists('nroer_pro')):
		print("Deleting the existing index for reindexing")
		res = es.indices.delete(index='nroer_pro')
		print("The delete response is %s " % res)

	request_body = {
			"settings": {
				"number_of_shards": 1,
				"number_of_replicas": 0,
				"analysis": {
					"analyzer": {
						"trigram": {
							"type": "custom",
							"tokenizer": "standard",
							"stopwords": "_english_",
							"filter": [
								"standard",
								"lowercase",
								"shingle"
							],
							"char_filter": ["html_strip"],
						},
						# "reverse": {
						# 	"type": "custom",
						# 	"tokenizer": "standard",
						# 	"filter": ["standard", "reverse"]
						# }
					},
					"filter": {
						# "stopwords": {
						# 	"type": "stop",
						# 	"ignore_case": True,
						# 	"stopwords": "_english_"
						# },
						"shingle": {
							"type": "shingle",
							"min_shingle_size": 2,
							"max_shingle_size": 3
						}
					},
				}
			},
			"mappings": {

				"Author": {
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"image": {		#all those Gsystem docs that have mime_type as null
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"video": {		#all those Gsystem docs that have mime_type as null
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"text": {		#all those Gsystem docs that have mime_type as null
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"application": {		#all those Gsystem docs that have mime_type as null
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"audio": {		#all those Gsystem docs that have mime_type as null
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"NotMedia": {		#all those Gsystem docs that have mime_type as null
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"Filehive": {
					"properties": {
						"filename": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}					
						}
					}
				},
				"RelationType": {	#one doc has content as null so the custom analyzer may not be required
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"Group": {
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"AttributeType": {
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"altnames":{
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"content": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				},
				"GAttribute": {
					"properties": {
						"name": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						},
						"tags": {
							"type": "text",
							"fields": {
								"trigram": {
									"type": "text",
									"analyzer": "trigram"
								},
								# "reverse": {
								# 	"type": "text",
								# 	"analyzer": "reverse"
								# }
							}
						}
					}
				}
			}
	}

	res = es.indices.create(index='nroer_pro', body=request_body)
	print("Response for index creation")
	print(res)

	dir = '/home/dvjsm/Gstudio/nroer/rcs-repo/'
	index_directory(dir)

main()

#for search, consider for the time being GSystem, Author, Group



# from elasticsearch import Elasticsearch
# import os
# import sys
# import json

# es = Elasticsearch("http://elsearch:changeit@localhost:9200")
# index_type = ""

# def index_directory(dir):
# 	k = 1
# 	for path, dirs, files in os.walk(dir):
# 		for file in files:
# 			fname = os.path.join(path,file)
# 			ext = (fname.rsplit('.',1))[1]
# 			if(ext=='json'):
# 				index_file(fname,k)
# 				k+=1

# def index_file(fname,k):
# 	with open(fname, 'r') as fp:
# 		try:
# 			document = json.load(fp)
# 		except:
# 			print("doc is empty")
# 			return
# 		else:
# 			print(fname)

# 	document["id"] = document.pop("_id")
# 	document["type"] = document.pop("_type")
# 	if("object_value" in document.keys()):
# 		document["object_value"] = str(document["object_value"])	#for consistent mapping 

# 	print("now indexing")
# 	if document["type"]=="GSystem":
# 		if('if_file' in document.keys()):
# 			if document["if_file"]["mime_type"] is not None:
# 				data = document["if_file"]["mime_type"].split("/")
# 				index_type = data[0]
# 			else:
# 				index_type = "NotMedia"
# 		else:
# 			index_type = "NotMedia"
# 		#index_type = "GSystem"			
# 	elif document["type"]=="Author":
# 		index_type = "Author"
# 	elif document["type"]=="GAttribute":
# 		index_type = "GAttribute"
# 	elif document["type"]=="GRelation":
# 		index_type = "GRelation"
# 	elif document["type"]=="AttributeType":
# 		index_type = "AttributeType"
# 	elif document["type"]=="Filehive":
# 		index_type = "Filehive"
# 	elif document["type"]=="RelationType":
# 		index_type = "RelationType"
# 	elif document["type"]=="Group":
# 		index_type = "Group"
# 	else:
# 		index_type = "DontCare"

# 	es.index(index='nroer_pro', doc_type=index_type, id=document["id"]["$oid"], body=json.dumps(document))
# 	print("indexed document %d" % k)

# def main():
# 	print("Starting the indexing process")

# 	if(es.indices.exists('nroer_pro')):
# 		print("Deleting the existing index for reindexing")
# 		res = es.indices.delete(index='nroer_pro')
# 		print("The delete response is %s " % res)

# 	request_body = {
# 			"settings": {
# 				"number_of_shards": 1,
# 				"number_of_replicas": 0,
# 				"analysis": {
# 					"analyzer": {
# 						"trigram": {
# 							"filter": [
# 								"lowercase",
# 								# "stopwords",
# 								"shingle"
# 							],
# 							"char_filter": ["html_strip"],
# 							"type": "custom",
# 							"tokenizer": "standard",
# 						},
# 						"reverse": {
# 							"type": "custom",
# 							"tokenizer": "standard",
# 							"filter": ["standard", "reverse"]
# 						}
# 					},
# 					"filter": {
# 						# "stopwords": {
# 						# 	"type": "stop",
# 						# 	"stopwords": [
# 						# 		"_english_"
# 						# 	]
# 						# },
# 						"shingle": {
# 							"type": "shingle",
# 							"min_shingle_size": 2,
# 							"max_shingle_size": 3
# 						}
# 					},
# 				}
# 			},
# 			"mappings": {

# 				"Author": {
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"image": {		#all those Gsystem docs that have mime_type as null
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"video": {		#all those Gsystem docs that have mime_type as null
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"text": {		#all those Gsystem docs that have mime_type as null
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"application": {		#all those Gsystem docs that have mime_type as null
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"audio": {		#all those Gsystem docs that have mime_type as null
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"NotMedia": {		#all those Gsystem docs that have mime_type as null
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"analyzer": "trigram",
# 							"search_analyzer": "standard"
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"Filehive": {
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"filename": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"analyzer": "trigram",
# 					        "search_analyzer": "standard",
# 						},
# 					}
# 				},
# 				"RelationType": {	#one doc has content as null so the custom analyzer may not be required
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"Group": {
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"AttributeType": {
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"altnames":{
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"content": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}
# 				},
# 				"GAttribute": {
# 					"_all": {
# 						"type": "text",
# 						"analyzer": "trigram",
# 						"search_analyzer": "standard"
# 					},
# 					"properties": {
# 						"name": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						},
# 						"tags": {
# 							"type": "text",
# 							"include_in_all": True,
# 							"search_analyzer": "standard",
# 							"analyzer": "trigram",
# 						}
# 					}

# 				}
# 			}
# 	}

# 	res = es.indices.create(index='nroer_pro', body=request_body)
# 	print("Response for index creation")
# 	print(res)

# 	dir = '/home/dvjsm/Gstudio/nroer/rcs-repo/'
# 	index_directory(dir)

# main()