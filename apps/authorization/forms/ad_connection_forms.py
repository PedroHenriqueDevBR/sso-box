from django import forms
from apps.authorization.models import ADConnection


class ADConnectionForm(forms.ModelForm):

    class Meta:
        model = ADConnection
        fields = '__all__'
    