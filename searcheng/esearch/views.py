from django.shortcuts import render
from django.http import HttpResponseRedirect
from elasticsearch import Elasticsearch		
import re
from .forms import SearchForm

es = Elasticsearch(['http://elsearch:changeit@localhost:9200'])
author_map = {}
f = open("esearch/author_mappings.txt","r")
authors = f.readlines()
for l in authors:
	k = l.split(':')
	auth_name = (k[1].split(';'))[1]
	author_map[str(auth_name)] = k[0] #post gre sql ids
f.close()
def resources_in_group(res,group_select):
	results = []
	returnList = []
	count=0
	group_id = str(group_select)
	print(group_id)
	for i in res["hits"]["hits"]:
		if "group_set" in i["_source"].keys():
			print("inloop")
			print(count)
			count+=1
			k = i["_source"]["group_set"]
			print(k)
			for j in k:
				if group_id == j["$oid"]:
					results.append(i)

	# for i in results:
	# 	if('if_file' in i.keys()):
	# 		s = i['name']
	# 		if '.' in s
	# 			l=s.index('.')
	# 		else:
	# 			l=len(s)
	print("for groups")
	print(results)
	return results

def get_search(request):
	flag = 0 
	#if the search button is pressed, it is a POST request
	res1_list = [];
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			#retrieving the query text in search box
			query = form.cleaned_data['query']
			print(query)
			query_display = ""
			select = request.POST['select']
			group_select = request.POST['group_select']


			if group_select=="all" and select!="Author":
				pass
			elif select=="Author":
				get_contributions(select,group_select,query)
			elif group_select!="all"and select!="Author":
				pass

			if(select=="all"):
				select = "Author,image,video,text,application,audio,NotMedia"


			phsug_name = get_suggestion_body(query,field_value = "name.trigram",slop_value = 2,field_name_value = "name")
			phsug_content = get_suggestion_body(query,field_value = "content.trigram",slop_value = 3,field_name_value = "content")
			phsug_tags = get_suggestion_body(query,field_value = "tags.trigram",slop_value = 2,field_name_value = "tags")




		queryNameInfo = [0,0.0,"",""] #[queryNameInfo[0],queryNameInfo[1],queryNameInfo[2],query_display_name]
		queryContentInfo = [0,0.0,"",""]
		queryTagsInfo = [0,0.0,"",""]
		# queryNameInfo[1],queryContentInfo[1],queryTagsInfo[1] = 0.0,0.0,0.0											#scores of first item in suggestions list with collate_match=True
		# queryNameInfo[2],queryContentInfo[2],queryTagsInfo[2]="","",""								#the top search query with collate_match=true suggested by phsug_name, phsug_content, phsug_tags suggest bodies
		# query_display_name,query_display_content,query_display_tags="","",""		

		get_suggestion(phsug_name,queryNameInfo,select,query)
		get_suggestion(phsug_content,queryContentInfo,select,query)
		get_suggestion(phsug_tags,queryTagsInfo,select,query)

		#print(res)
		print (queryNameInfo[0],queryContentInfo[0],queryTagsInfo[0])
		query_display = ""

		#what if all are 1 and 2/3 names are same but the third one has higher score
		if((queryNameInfo[0]==1 and queryNameInfo[2]==query) or (queryContentInfo[0]==1 and queryContentInfo[2]==query) or (queryTagsInfo[0]==1 and queryTagsInfo[2]==query)): 
			#if the original query is the query to be searched
			query_display = query
		elif(queryNameInfo[0]==0 and queryContentInfo[0]==0 and queryTagsInfo[0]==0):																		
			#if we didnt find any suggestion, neither did we find the query already indexed->query remains same
			query_display = query
		else: #if we found a suggestion 
			res1_list = ['Search instead for <a href="">%s</a>'%(query)] #if the user still wants to search for the original query he asked for
			if(queryNameInfo[1]>=queryContentInfo[1] and queryNameInfo[1]>=queryTagsInfo[1]):						 #comparing the scores of name,content,tags suggestions and finding the max of the three
				query = queryNameInfo[2]
				query_display = queryNameInfo[3]					 #what query to display on the search result screen
			if(queryContentInfo[1]>queryNameInfo[1] and queryContentInfo[1]>=queryTagsInfo[1]):
				query = queryContentInfo[2]
				query_display = queryContentInfo[3]
			if(queryTagsInfo[1]>queryContentInfo[1] and queryTagsInfo[1]>queryNameInfo[1]):
				query = queryTagsInfo[2]
				query_display = queryTagsInfo[3]

		if(queryNameInfo[0]==0 and queryContentInfo[0]==0 and queryTagsInfo[0]==0):#if we didnt find any suggestion, neither did we find the query already indexed
			res = es.search(index="nroer_pro",doc_type=select, body={"query": {
																		"multi_match": { 											#first do a multi_match
																			"query" : query,
																			"type": "best_fields",									#when multiple words are there in the query, try to search for those words in a single field
																			"fields": ["name^3", "altnames", "content^2", "tags"],	#in which field to search the query
																			"minimum_should_match": "30%"
																			}
																		},
																	"rescore": {													#rescoring the top 50 results of multi_match
																		"window_size": 50,
																		"query": {
																			"rescore_query": {
																				"bool": {											#rescoring using match phrase
																					"should": [
																						{"match_phrase": {"name": { "query": query, "slop":2}}},
																						{"match_phrase": {"altnames": { "query": query, "slop": 2}}},
																						{"match_phrase": {"content": { "query": query, "slop": 4}}}
																					]
																				}
																			}
																		}
																	}
																})

		else: #if we found a suggestion or if the query exists as a phrase in one of the name/content/tags field
			res = es.search(index="nroer_pro",doc_type=select, body={"query": {
																		"multi_match": {
																			"query": query,
																			"fields": ["name^3", "altnames", "content^2", "tags"],
																			"type": "phrase", #we are doing a match phrase on multi field.
																			"slop": 5
																		}
																	}
																})

		if group_select!="all"and select!="Author":
			restrial = resources_in_group(res,group_select)

		hits = "No of docs found: %d" % res['hits']['total']
		res_list = ['Showing results for %s :' % query_display, hits]
		res_list = ['Showing results for %s :' % query_display]
		#med_list is the list which will be passed to the html file.
		med_list = []
		for doc in res['hits']['hits']:					
			if('if_file' in doc['_source'].keys()):
				s = doc['_source']['name']
				if '.' in s:
					l = s.index('.')
				else:
					l = len(s)
				med_list.append([doc['_id'],s[0:l],doc['_source']['if_file']['original']['relurl'],doc['_score'],doc['_source']['content']])	#printing only the id for the time being along with the node name
			else:
				med_list.append([doc['_id'],doc['_source']['name'],None,doc['_score'],doc['_source']['content']])
		
		if(len(res1_list)>0):
			return render(request, 'esearch/basic.html', {'header':res_list, 'alternate': res1_list, 'content': med_list})
		return render(request, 'esearch/basic.html', {'header':res_list, 'content': med_list})
		return render()
#if the search page is loaded for the first time
	else:
		form = SearchForm()

	return render(request, 'esearch/sform.html', {'form':form})

def get_contributions(select,group_select,author_name):
	author_name+='\n'
	i = 0
	doc_types = ['image','video','text','application','audio','NotMedia']
	try:
		sql_id = int(author_map[str(author_name)])
	except:
		return []
	else:
		resultSet = []
		while(True):
			body = {
				"query":{
					"match_all":{}
				},
				"from":i,
				"size":100
			}
			res = es.search(index = "nroer_pro",body = body)
			l = len(res["hits"]["hits"])
			if l > 0:
				for doc in (res['hits']['hits']):
					#is it possible that an author has contributed to a paper that does not belong to any group
					if ("group_set" in (doc["_source"]).keys()) and ("contributors" in (doc["_source"]).keys()):
						group_set = []
						for group_id in doc["_source"]["group_set"]:
							group_set.append(group_id["$oid"])
						contributors = doc["_source"]["contributors"]
						if group_select == "all":
							if sql_id in contributors and doc["_source"]["type"] in doc_types:
								resultSet.append(doc)

						else:
							if (sql_id in contributors) and (group_select in group_set) and doc["_source"]["type"] in doc_types:
								resultSet.append(doc)
			else:
				break
			i+=100
		return resultSet
	

def get_suggestion_body(query,field_value,slop_value,field_name_value):
	phrase_suggest = {												#json body of phrase suggestion in name field
		"suggest": {
			"text": query,										#the query for which we want to find suggestion
			#"simple_phrase": {
				"phrase": {											
					"field": field_value,					#in which indexed field to find the suggestion
					"gram_size": 3,								#this is the max shingle size
					"max_errors": 2,							#the maximum number of terms that can be misspelt in the query
					"direct_generator": [ {
			          "field": field_value,
			          #"suggest_mode": "missing",
			          "min_word_length": 2,
					  "prefix_length": 0,						#misspelling in a single word may exist in the first letter itself
			          "suggest_mode":"missing"					#search for suggestions only if the query isnt present in the index
			        } ],
			        "highlight": {								#to highlight the suggested word
			          "pre_tag": "<em>",
			          "post_tag": "</em>"
			        },
			        "collate": {								#this is used to check if the returned suggestion exists in the index
			        	"query": {
			        		"inline": {
			        			"match_phrase": {				#matching the returned suggestions with the existing index
			        				"{{field_name}}": {
				        				"query": "{{suggestion}}",
				        				"slop": slop_value					
				        			}
			        			}
			        		}
			        	},
			        	"params": {"field_name": field_name_value},
			        	"prune": True							#to enable collate_match of suggestions
			        }
				},
			}
		}
	return phrase_suggest


def get_suggestion(suggestion_body,queryInfo,doc_types,query):
	res = es.suggest(body=suggestion_body, index='nroer_pro')						#first we search for suggestion in the name field as it has the highest priority
	print(res)																					
	if(len(res['suggest'][0]['options'])>0):									#if we get a suggestion means the phrase doesnt exist in the index
		for sugitem in res['suggest'][0]['options']:
			if sugitem['collate_match'] == True:								#we find the suggestion with collate_match = True
				queryInfo[0] = 1
				queryInfo[1] = sugitem['score']
				queryInfo[2] = sugitem['text']				
				queryInfo[3] = sugitem['highlighted']						#the query to be displayed onto the search results screen
				#print(res)
				break
	else:						#should slop be included in the search part here?
		query_body = {"query":{"match_phrase":{"name": query,}}}
		if(es.search(index='nroer_pro',doc_type=doc_types,body=query_body)['hits']['total']>0):
			queryInfo[0] = 1							#set queryNameInfo[0] = 1 when we found a suggestion or we found a hit in the indexed data
			queryInfo[2] = query




# phsug_content = {											#json body of phrase suggestion in content field
# 	"suggest": {
# 		"text": query,
# 		"phrase": {
# 				"field": "content.trigram",
# 				"gram_size": 3,
# 				"max_errors": 2,
# 				"direct_generator": [ {
# 		          "field": "content.trigram",
# 		          "min_word_length": 2,
# 				  "prefix_length": 0,
# 		          "suggest_mode": "missing"
# 		        } ],
# 		        "highlight": {
# 		          "pre_tag": "<em>",
# 		          "post_tag": "</em>"
# 		        },
# 		        "collate": {
# 		        	"query": {
# 		        		"inline": {
# 		        			"match_phrase": {
# 		        				"{{field_name}}": {
# 			        				"query": "{{suggestion}}",
# 			        				"slop": 3
# 			        			}
# 		        			}
# 		        		}
# 		        	},
# 		        	"params": {"field_name": "content"},
# 		        	"prune": True
# 		        }
# 			},
# 		}