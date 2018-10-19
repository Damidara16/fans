from django import forms
from .models import Points, Plan
from banking.models import TransactionHistory

class SetPoint(forms.ModelForm):
    class Meta:
        model = Points
        fields = ('likes', 'comment')


class MakeTip(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        fields = ('amount', 'description')

class MakePlan(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ('price', 'description')
