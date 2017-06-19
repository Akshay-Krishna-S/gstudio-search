from django.shortcuts import render
from django.http import HttpResponseRedirect
from elasticsearch import Elasticsearch		
import re

from .forms import SearchForm

es = Elasticsearch(['http://elsearch:changeit@localhost:9200'])


def get_search(request):
	#if the search button is pressed, it is a POST request
	res1_list = []; fname = 0; fcontent =0; ftags = 0;
	if request.method == 'POST':
		form = SearchForm(request.POST)
		# if form.is_valid():
		# 	#retrieving the query text in search box
		# 	query = form.cleaned_data['query']
		# 	print(query)
		# 	query_display = ""
		# 	select = request.POST['select'] #for filtering our search results
		# 	if(select=="all"):				#to search across all records
		# 		select = "Author,image,video,text,application,audio,NotMedia"

		# 	# suggestion = {
		# 	# 	"entity-suggest": {
		# 	# 		"text": query,
		# 	# 		"term": {
		# 	# 			#"analyzer": "standard",
		# 	# 			"field":"name",
		# 	# 			"min_word_length": 2,
		# 	# 			"prefix_length": 0
		# 	# 		},
		# 	# 		"term": {
		# 	# 			#"analyzer": "standard",
		# 	# 			"field": "altnames",
		# 	# 			"min_word_length": 2,
		# 	# 			"prefix_length": 0
		# 	# 		},
		# 	# 		"term": {
		# 	# 			#"analyzer": "standard",
		# 	# 			"field": "content",
		# 	# 			"min_word_length": 2,
		# 	# 			"prefix_length": 0
		# 	# 		},
		# 	# 		"term": {
		# 	# 			#"analyzer": "standard",
		# 	# 			"field": "tags",
		# 	# 			"min_word_length": 2,
		# 	# 			"prefix_length": 0
		# 	# 		}
		# 	# 	}
		# 	# }
		# 	phsug_name = {												#json body of phrase suggestion in name field
		# 		"suggest": {
		# 			"text": query,										#the query for which we want to find suggestion
		# 			#"simple_phrase": {
		# 				"phrase": {											
		# 					"field": "name.trigram",					#in which indexed field to find the suggestion
		# 					"gram_size": 3,								#this is the max shingle size
		# 					"max_errors": 2,							#the maximum number of terms that can be misspelt in the query
		# 					"direct_generator": [ {
		# 			          "field": "name.trigram",
		# 			          #"suggest_mode": "missing",
		# 			          "min_word_length": 2,
		# 					  "prefix_length": 0,						#misspelling in a single word may exist in the first letter itself
		# 			          "suggest_mode":"missing"					#search for suggestions only if the query isnt present in the index
		# 			        } ],
		# 			        "highlight": {								#to highlight the suggested word
		# 			          "pre_tag": "<em>",
		# 			          "post_tag": "</em>"
		# 			        },
		# 			        "collate": {								#this is used to check if the returned suggestion exists in the index
		# 			        	"query": {
		# 			        		"inline": {
		# 			        			"match_phrase": {				#matching the returned suggestions with the existing index
		# 			        				"{{field_name}}": {
		# 				        				"query": "{{suggestion}}",
		# 				        				"slop": 2					
		# 				        			}
		# 			        			}
		# 			        		}
		# 			        	},
		# 			        	"params": {"field_name": "name"},
		# 			        	"prune": True							#to enable collate_match of suggestions
		# 			        }
		# 			},
		# 	}
		# }
		# 			#"simple_phrase": {
		# 			# 	"phrase": {
		# 			# 		"field": "altnames.trigram",
		# 			# 		"gram_size": 3,
		# 			# 		"max_errors": 2,
		# 			# 		"direct_generator": [ {
		# 			#           "field": "altnames.trigram",
		# 			#           "min_word_length": 2,
		# 			# 		  "prefix_length": 0,
		# 			#           "suggest_mode": "missing"
		# 			#         } ],
		# 			#         "highlight": {
		# 			#           "pre_tag": "<em>",
		# 			#           "post_tag": "</em>"
		# 			#         }
		# 			# 	#}
		# 			# },
		# 			#}
		# 	phsug_content = {											#json body of phrase suggestion in content field
		# 		"suggest": {
		# 			"text": query,
		# 			"phrase": {
		# 					"field": "content.trigram",
		# 					"gram_size": 3,
		# 					"max_errors": 2,
		# 					"direct_generator": [ {
		# 			          "field": "content.trigram",
		# 			          "min_word_length": 2,
		# 					  "prefix_length": 0,
		# 			          "suggest_mode": "missing"
		# 			        } ],
		# 			        "highlight": {
		# 			          "pre_tag": "<em>",
		# 			          "post_tag": "</em>"
		# 			        },
		# 			        "collate": {
		# 			        	"query": {
		# 			        		"inline": {
		# 			        			"match_phrase": {
		# 			        				"{{field_name}}": {
		# 				        				"query": "{{suggestion}}",
		# 				        				"slop": 3
		# 				        			}
		# 			        			}
		# 			        		}
		# 			        	},
		# 			        	"params": {"field_name": "content"},
		# 			        	"prune": True
		# 			        }
		# 			},
		# 		}
		# 	}

		# 	phsug_tags = {												#json body of phrase suggestion in content field
		# 		"suggest": {
		# 			"text": query,
		# 			"phrase": {
		# 					"field": "tags.trigram",
		# 					"gram_size": 3,
		# 					"max_errors": 2,
		# 					"direct_generator": [ {
		# 			          "field": "tags.trigram",
		# 			          "min_word_length": 2,
		# 					  "prefix_length": 0,
		# 			          "suggest_mode": "missing"
		# 			        } ],
		# 			        "highlight": {
		# 			          "pre_tag": "<em>",
		# 			          "post_tag": "</em>"
		# 			        },
		# 			        "collate": {
		# 			        	"query": {
		# 			        		"inline": {
		# 			        			"match_phrase": {
		# 			        				"{{field_name}}": {
		# 				        				"query": "{{suggestion}}",
		# 				        				"slop": 2
		# 				        			}
		# 			        			}
		# 			        		}
		# 			        	},
		# 			        	"params": {"field_name": "tags"},
		# 			        	"prune": True
		# 			        }
		# 			},
		# 		}
		# 	}
		# # res = es.suggest(body=suggestion, index='nroer_pro')
		# # print(res)
		# # if(" " not in query):
		# # 	res = es.suggest(body=suggestion, index='nroer_pro')
		# # 	print(res)
		# # 	if(len(res['entity-suggest'][0]['options'])>0):
		# # 		res1_list = ['Search instead for <a href="">%s</a>'%(query)]
		# # 		query = res['entity-suggest'][0]['options'][0]['text']
		# # 		query_display = '<em>'+query+'</em>'
		# # 		print("fuck", query)

		# # else:
		# sname,scontent,stag = 0.0,0.0,0.0											#scores of first item in suggestions list with collate_match=True
		# query_name,query_content,query_tags="","",""								#the top search query with collate_match=true suggested by phsug_name, phsug_content, phsug_tags suggest bodies
		# query_display_name,query_display_content,query_display_tags="","",""		
		# res = es.suggest(body=phsug_name, index='nroer_pro')						#first we search for suggestion in the name field as it has the highest priority
		# print(res)																					
		# if(len(res['suggest'][0]['options'])>0):									#if we get a suggestion means the phrase doesnt exist in the index
		# 	for sugitem in res['suggest'][0]['options']:
		# 		if sugitem['collate_match'] == True:								#we find the suggestion with collate_match = True
		# 			query_name = sugitem['text']				
		# 			query_display_name = sugitem['highlighted']						#the query to be displayed onto the search results screen
		# 			sname = sugitem['score']
		# 			fname = 1
		# 			#print(res)
		# 			break
		# else:						#should slop be included in the search part here?
		# 	if(es.search(index='nroer_pro',doc_type=select,body={"query": {
		# 															"match_phrase": {
		# 																"name": query,
		# 															}
		# 		}})['hits']['total']>0):
		# 		fname = 1															#set fname = 1 when we found a suggestion or we found a hit in the indexed data
		# 		query_name = query

		# #if(fname==0):
		# res = es.suggest(body=phsug_content, index='nroer_pro')
		# print(res)
		# if(len(res['suggest'][0]['options'])>0):
		# 	for sugitem in res['suggest'][0]['options']:
		# 		if sugitem['collate_match'] == True:
		# 			query_content = sugitem['text']
		# 			query_display_content = sugitem['highlighted']
		# 			scontent = sugitem['score']
		# 			fcontent = 1
		# 			break	
		# else:
		# 	if(es.search(index='nroer_pro',doc_type=select,body={"query": {
		# 														"match_phrase": {
		# 															"content": query,
		# 														}
		# 	}})['hits']['total']>0):
		# 		fcontent = 1
		# 		query_content = query

		# #if(fname==0 and fcontent==0):
		# res = es.suggest(body=phsug_tags, index='nroer_pro')
		# print(res)
		# if(len(res['suggest'][0]['options'])>0):
		# 	for sugitem in res['suggest'][0]['options']:
		# 		if sugitem['collate_match'] == True:
		# 			query_tags = sugitem['text']
		# 			query_display_tags = sugitem['highlighted']
		# 			stag = sugitem['score']
		# 			ftags = 1
		# 			break	
		# else:
		# 	if(es.search(index='nroer_pro',doc_type=select,body={"query": {
		# 														"match_phrase": {
		# 															"tags": query,
		# 														}
		# 	}})['hits']['total']>0):
		# 		ftags = 1
		# 		query_tags = query

		# #print(res)
		# print (fname,fcontent,ftags)
		# 	# if(len(res['suggest'][0]['options'])>0):
		# 	# 	for sugitem in res['suggest'][0]['options']:
		# 	# 		if sugitem['collate_match'] == True:
		# 	# 			query = sugitem['text']
		# 	# 			query_display = sugitem['highlighted']
		# 	# 			res1_list = ['Search instead for <a href="">%s</a>'%(query)]
		# 	# 			break
		# 	# 	if query_display==query:
		# 	# 		print("no collate match")
		# 	# 		query = res['suggest'][0]['options'][0]['text']

		# 	# else:
		# 	# 	newq += qitem+" "
		# 	# query = newq
		# 	# print(query)
		# 	# if(len(res['suggest'][0]['options'])>0):
		# 	# 	query = (res['suggest'][0]['options'][0])['text']
		
		# #what if all are 1 and 2/3 names are same but the third one has higher score
		# if((fname==1 and query_name==query) or (fcontent==1 and query_content==query) or (ftags==1 and query_tags==query)): 
		# 	#if the original query is the query to be searched
		# 	query_display = query
		# elif(fname==0 and fcontent==0 and ftags==0):																		
		# 	#if we didnt find any suggestion, neither did we find the query already indexed->query remains same
		# 	query_display = query
		# else: #if we found a suggestion 
		# 	res1_list = ['Search instead for <a href="">%s</a>'%(query)] #if the user still wants to search for the original query he asked for
		# 	if(sname>=scontent and sname>=stag):						 #comparing the scores of name,content,tags suggestions and finding the max of the three
		# 		query = query_name
		# 		query_display = query_display_name						 #what query to display on the search result screen
		# 	if(scontent>sname and scontent>=stag):
		# 		query = query_content
		# 		query_display = query_display_content
		# 	if(stag>scontent and stag>sname):
		# 		query = query_tags
		# 		query_display = query_display_tags

		# if(fname==0 and fcontent==0 and ftags==0):#if we didnt find any suggestion, neither did we find the query already indexed
		# 	res = es.search(index="nroer_pro",doc_type=select, body={"query": {
		# 																"multi_match": { 											#first do a multi_match
		# 																	"query" : query,
		# 																	"type": "best_fields",									#when multiple words are there in the query, try to search for those words in a single field
		# 																	"fields": ["name^3", "altnames", "content^2", "tags"],	#in which field to search the query
		# 																	"minimum_should_match": "30%"
		# 																	}
		# 																},
		# 															"rescore": {													#rescoring the top 50 results of multi_match
		# 																"window_size": 50,
		# 																"query": {
		# 																	"rescore_query": {
		# 																		"bool": {											#rescoring using match phrase
		# 																			"should": [
		# 																				{"match_phrase": {"name": { "query": query, "slop":2}}},
		# 																				{"match_phrase": {"altnames": { "query": query, "slop": 2}}},
		# 																				{"match_phrase": {"content": { "query": query, "slop": 4}}}
		# 																			]
		# 																		}
		# 																	}
		# 																}
		# 															}
		# 														})

		# else: #if we found a suggestion or if the query exists as a phrase in one of the name/content/tags field
		# 	res = es.search(index="nroer_pro",doc_type=select, body={"query": {
		# 																"multi_match": {
		# 																	"query": query,
		# 																	"fields": ["name^3", "altnames", "content^2", "tags"],
		# 																	"type": "phrase", #we are doing a match phrase on multi field.
		# 																	"slop": 5
		# 																}
		# 															}
		# 														})
		# hits = "No of docs found: %d" % res['hits']['total']
		# res_list = ['Showing results for %s :' % query_display, hits]
		# #med_list is the list which will be passed to the html file.
		# med_list = []
		# for doc in res['hits']['hits']:					
		# 	if('if_file' in doc['_source'].keys()):
		# 		s = doc['_source']['name']
		# 		if '.' in s:
		# 			l = s.index('.')
		# 		else:
		# 			l = len(s)
		# 		med_list.append([doc['_id'],s[0:l],doc['_source']['if_file']['original']['relurl'],doc['_score'],doc['_source']['content']])	#printing only the id for the time being along with the node name
		# 	else:
		# 		med_list.append([doc['_id'],doc['_source']['name'],None,doc['_score'],doc['_source']['content']])

		# if(len(res1_list)>0):
		# 	return render(request, 'esearch/basic.html', {'header':res_list, 'alternate': res1_list, 'content': med_list})
		# return render(request, 'esearch/basic.html', {'header':res_list, 'content': med_list})
		return render()
#if the search page is loaded for the first time
	else:
		form = SearchForm()

	return render(request, 'esearch/sform.html', {'form':form})


# phsug = {
# 				"suggest": {
# 					"text": query,
# 						"phrase": {
# 							"field": "name.trigram",
# 							"min_word_length": 2,
# 							"prefix_length": 0,
# 							"gram_size": 3,
# 							"direct_generator": [ {
# 					          "field": "name.trigram",
# 					          "suggest_mode": "missing"
# 					        } ],
# 					        "highlight": {
# 					          "pre_tag": "<em>",
# 					          "post_tag": "</em>"
# 					        }
# 						},
# 						"phrase": {
# 							"field": "altnames.trigram",
# 							"min_word_length": 2,
# 							"prefix_length": 0,
# 							"gram_size": 3,
# 							"direct_generator": [ {
# 					          "field": "altnames.trigram",
# 					          "suggest_mode": "missing"
# 					        } ],
# 					        "highlight": {
# 					          "pre_tag": "<em>",
# 					          "post_tag": "</em>"
# 					        }
# 						},
# 						"phrase": {
# 							"field": "content.trigram",
# 							"min_word_length": 2,
# 							"prefix_length": 0,
# 							"gram_size": 3,
# 							"direct_generator": [ {
# 					          "field": "content.trigram",
# 					          "suggest_mode": "missing"
# 					        } ],
# 					        "highlight": {
# 					          "pre_tag": "<em>",
# 					          "post_tag": "</em>"
# 					        }
# 						},
# 						"phrase": {
# 							"field": "tags",
# 							# "min_word_length": 2,
# 							# "prefix_length": 0,
# 							"gram_size": 3,
# 							"direct_generator": [ {
# 					          "field": "tags",
# 					          "suggest_mode": "missing",
# 					          "prefix_length": 0,
# 					          "min_word_length": 2,
# 					        } ],
# 					        "highlight": {
# 					          "pre_tag": "<em>",
# 					          "post_tag": "</em>"
# 					        }
# 						}
# 					}
# 			}
