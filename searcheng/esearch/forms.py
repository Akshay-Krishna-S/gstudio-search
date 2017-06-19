from django import forms

CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio")]

class SearchForm(forms.Form):
	query = forms.CharField(label = 'Query')
	group_select = forms.ChoiceField(label = "Select Group",widget=forms.Select, choices=GROUP_CHOICES)
	select = forms.ChoiceField(label = "Filter",widget=forms.Select, choices=CHOICES)
