from django import forms
from .models import Notfication

class NotficationForm(forms.ModelForm):

    class Meta:
        model = Notfication
        fields = ('new_sub','re_subbed','like','comment','points_add','points_spent','transactions','tip',)
