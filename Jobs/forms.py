from django import forms

class searchForm(forms.Form):
  queryString = forms.CharField(max_length = 100)
  location = forms.CharField(max_length = 100)