from django.shortcuts import render
from django.http import HttpResponseRedirect
from elasticsearch import Elasticsearch		
import json

from .forms import SearchForm

es = Elasticsearch(['http://elsearch:changeit@localhost:9200'])


def get_search(request):

	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']
			res = es.search(index="gstudio", body={"query": {"multi_match": {
														"query": query,
														"type": "best_fields",
														"fields": ["name^2", "altnames", "content"]
				}}})
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
					med_list.append([doc['_id'],s[0:l],doc['_source']['if_file']['original']['relurl']])	#printing only the id for the time being along with the node name
				else:
					med_list.append([doc['_id'],doc['_source']['name'],None])

			return render(request, 'esearch/basic.html', {'header':res_list, 'content': med_list})

	else:
		form = SearchForm()

	return render(request, 'esearch/sform.html', {'form':form})
