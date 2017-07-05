from django import forms
import os 
import json
CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio")]
GROUP_CHOICES=[]
GROUP_CHOICES.append(("all","All"))
group_map = {}
attribute_map = {}
ATTRIBUTE_CHOICES = [("--Select--","--Select--"),("interactivitytype","Interactivity type"),("educationaluse","Educational use"),("educationalsubject","Educational subject"),("educationallevel","Educational Level"),("source","Source"),("audience","Audience"),("educationalalignment","Educational alignment"),]
# educationaluse_choices = []
# interactivitytype_choices = []
# educationalsubject_choices = []
# educationallevel_choices = []
# source_choices = []
# audience_choices = []
# educationalalignment_choices = []
secondlevel_choices = []

with open("esearch/attribute_map.json") as am:
	attribute_map = json.load(am)



with open("/home/vignesh/Desktop/PS1-Codes/groupmap.json", 'r') as gm:
	group_map = json.load(gm)

for i in ATTRIBUTE_CHOICES:
	if i[0] != '--Select--':
		l = []
		for val in attribute_map[i[0]]:
			tup = (val,val)
			l.append(tup)
		secondlevel_choices.append(l)


for l in group_map.keys():
	tup = (l, group_map[l])
	tup = tuple(tup)
	GROUP_CHOICES.append(tup)

class SearchForm(forms.Form):
	query = forms.CharField(label = '', widget = forms.TextInput(attrs={'placeholder': 'Search for'}), error_messages = False)
	group = forms.ChoiceField(label = "Group", widget = forms.Select, choices = GROUP_CHOICES)
	select = forms.ChoiceField(label = "Filter", widget = forms.Select, choices = CHOICES)

class AdvancedSearchForm(forms.Form):
	query = forms.CharField(label = 'Query')
	attribute_select = forms.ChoiceField(label = "Select Attribute",widget=forms.Select, choices=ATTRIBUTE_CHOICES)
	educationaluse_choices = forms.ChoiceField(label = "Select educational use",widget=forms.Select, choices=secondlevel_choices[0])
	interactivitytype_choices = forms.ChoiceField(label = "Select activity type",widget=forms.Select, choices=secondlevel_choices[1])
	educationalsubject_choices = forms.ChoiceField(label = "Select subject",widget=forms.Select, choices=secondlevel_choices[2])
	educationallevel_choices = forms.ChoiceField(label = "Select level",widget=forms.Select, choices=secondlevel_choices[3])
	source_choices = forms.ChoiceField(label = "Select source",widget=forms.Select, choices=secondlevel_choices[4])
	audience_choices = forms.ChoiceField(label = "Select audience",widget=forms.Select, choices=secondlevel_choices[5])
	educationalalignment_choices = forms.ChoiceField(label = "Select alignment",widget=forms.Select, choices=secondlevel_choices[6])