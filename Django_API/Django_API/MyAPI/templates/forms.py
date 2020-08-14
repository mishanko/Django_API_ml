from django import forms

class SentimentForm(forms.Form):
    review=forms.CharField(max_length=15000, widget=forms.TextInput(attrs={'placeholder': "Enter Review"}))
