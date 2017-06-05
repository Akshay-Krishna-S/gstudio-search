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
			#query = form.cleaned_data['searchq']
			query = request.POST['query']
			select = request.POST['select']
			if(select=="all"):
				select = ""
			res = es.search(index="gstudio",doc_type=select, body={
														"from":0,"size":100,
														"query": 
															{"multi_match": 
																{
																	"query": query,
																	"type": "best_fields",
																	"fields": ["name^2", "altnames", "content"]
																}
															}
													})
			hits = "No of docs found: %d" % res['hits']['total']
			result = []
			#result.append(hits)
			for doc in res['hits']['hits']:
				#result = result + doc['_id'] + "\n"
				result.append(doc["_id"] + ":" + doc["_source"]["name"])
				#if(doc["_type"] == "image" ):
				#	result.append("/home/nazgul/Ashwin/data/media/"+doc["_source"]["if_file"]["thumbnail"]["relurl"])

			return render(request, 'esearch/basic.html', {'content': result})

	else:
		form = SearchForm()

	return render(request, 'esearch/sform.html', {'form':form})
