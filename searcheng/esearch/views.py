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
			for doc in res['hits']['hits']:
				res_list.append(doc['_id']+" : "+doc['_source']['name'])	#printing only the id for the time being along with the node name

			return render(request, 'esearch/basic.html', {'content': res_list})

	else:
		form = SearchForm()

	return render(request, 'esearch/sform.html', {'form':form})
