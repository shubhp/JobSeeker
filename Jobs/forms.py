from django import forms

class searchForm(forms.Form):
  queryString = forms.CharField(max_length = 100)
  searchAreaChoices = (
      ('LocationTag', 'Location'),
      ('Startup', 'Startup Name')
    )
  searchArea = forms.ChoiceField(choices = searchAreaChoices)