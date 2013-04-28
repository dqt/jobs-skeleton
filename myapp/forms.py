from django import forms

class SearchForm(forms.Form):
    jobtype = forms.CharField(max_length=100)
    location = forms.CharField()
