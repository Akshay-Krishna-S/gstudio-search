from django import forms

CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio")]
GROUP_CHOICES=[]
GROUP_CHOICES.append(("all","All"))

f = open("esearch/group_mappingsNROER.txt","r")
groups = f.readlines()
for l in groups:
	k=l.split(";")
	tup = (k[0],k[1])
	tup = tuple(tup)
	GROUP_CHOICES.append(tup)

class SearchForm(forms.Form):
	query = forms.CharField(label = 'Query')
	group_select = forms.ChoiceField(label = "Select Group",widget=forms.Select, choices=GROUP_CHOICES)
	select = forms.ChoiceField(label = "Filter",widget=forms.Select, choices=CHOICES)
