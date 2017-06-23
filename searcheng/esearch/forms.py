from django import forms
import os 
import json
CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio")]
GROUP_CHOICES=[]
GROUP_CHOICES.append(("all","All"))
group_map = {}

with open("/home/dvjsm/djanpro/groupmap.json", 'r') as gm:
	group_map = json.load(gm)

for l in group_map.keys():
	tup = (l, group_map[l])
	tup = tuple(tup)
	GROUP_CHOICES.append(tup)

class SearchForm(forms.Form):
	query = forms.CharField(label = '', widget = forms.TextInput(attrs={'placeholder': 'Search for'}), error_messages = False)
	group = forms.ChoiceField(label = "Group", widget = forms.Select, choices = GROUP_CHOICES)
	select = forms.ChoiceField(label = "Filter", widget = forms.Select, choices = CHOICES)