from django import forms


class FormSearch(forms.Form):
    search = forms.CharField(max_length=60, required=False ,widget=forms.TextInput(attrs={'class': 'form-control search-input',
                                                                    'type': 'search', 'placeholder': 'Localizar aqui...',
                                                                    'autocomplete': 'off'}))