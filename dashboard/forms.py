from django import forms



class PatientReport(forms.Form):
     start_date = forms.DateField(widget=forms.DateInput())
     end_date = forms.DateField(widget=forms.DateInput())