from django import forms

class FrequencyRangeForm(forms.Form):
    start_ul = forms.FloatField(label='Start (UL)')
    stop_ul = forms.FloatField(label='Stop (UL)')
