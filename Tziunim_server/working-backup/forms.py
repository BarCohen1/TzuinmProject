from django import forms
from django.utils.safestring import mark_safe

class WebsiteForm(forms.Form):
    single_prof = forms.CharField(label='Your website', label_suffix=': ', max_length=100, initial='http://', required=True)
