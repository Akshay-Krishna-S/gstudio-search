from django import forms

CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio")]

class SearchForm(forms.Form):
	query = forms.CharField(label = 'Query')
	group-select = forms.ChoiceField(label = "Group Select",widget=forms.Select, choices=GROUP_CHOICES)
	select = forms.ChoiceField(label = "Filter",widget=forms.Select, choices=CHOICES)
