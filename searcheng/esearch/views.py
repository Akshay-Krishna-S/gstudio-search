from django.shortcuts import render
from django.http import HttpResponseRedirect
from elasticsearch import Elasticsearch		
import re

from .forms import SearchForm

es = Elasticsearch(['http://elsearch:changeit@localhost:9200'])


def get_search(request):

	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']
			print(query)
			select = request.POST['select']
			if(select=="all"):
				select = ""

			res = es.search(index="nroer",doc_type=select, body={"query": {
																			"multi_match": {
																				"query" : query,
																				"type": "best_fields",
																				"fields": ["name^2", "altnames", "content", "tags"],
																				"minimum_should_match": "30%"
																				}
																			},
																	"rescore": {
																		"window_size": 50,
																		"query": {
																			"rescore_query": {
																				"bool": {
																					"should": [
																						{"match_phrase": {"name": { "query": query, "slop":50}}},
																						{"match_phrase": {"altnames": { "query": query, "slop": 50}}},
																						{"match_phrase": {"content": { "query": query, "slop": 50}}}
																					]
																				}
																			}
																		}
																	}
																})
			hits = "No of docs found: %d" % res['hits']['total']
			res_list = ['Result :', hits]
			med_list = []
			for doc in res['hits']['hits']:
				#if(doc['_source']['if_file'] in doc['_source'].keys()):
					# if(doc['_source']['if_file']['original']['relurl'] is not None):
					# 	med_list.append()					
				if('if_file' in doc['_source'].keys()):
					s = doc['_source']['name']
					if '.' in s:
						l = s.index('.')
					else:
						l = len(s)
					med_list.append([doc['_id'],s[0:l],doc['_source']['if_file']['original']['relurl'],doc['_score']])	#printing only the id for the time being along with the node name
				else:
					med_list.append([doc['_id'],doc['_source']['name'],None,doc['_score']])

			return render(request, 'esearch/basic.html', {'header':res_list, 'content': med_list})

	else:
		form = SearchForm()

	return render(request, 'esearch/sform.html', {'form':form})
