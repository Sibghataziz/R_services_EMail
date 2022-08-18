from cProfile import label
from django import forms

class NameForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    Content = forms.CharField(widget=forms.Textarea(attrs={'name':'Content', 'rows':'30', 'cols':'70'}))
    Emails = forms.CharField(widget=forms.Textarea(attrs={'name':'Emails', 'rows':'30', 'cols':'50'}))
    Your_Email = forms.EmailField()
    Your_Two_Factor_Password = forms.CharField(max_length=50)
    Username = forms.CharField(max_length=50)