from django import forms

CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio")]

class SearchForm(forms.Form):
	query = forms.CharField(label = 'Query')
	select = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
