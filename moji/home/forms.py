from django import forms
from django.conf import settings
from django.core.mail import send_mail

class Reporter(forms.Form):
    Report = (('bug', 'bug'), ('violation', 'violation'), ('support', 'support'), 'advice', 'advice')

    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=255, required=True)
    #add a choice to subject
    sub = ''

    #message = forms.ChoiceField(choices=Report)
    Subject = forms.CharField(max_length=55, required=True)

    def send_email(self):
        #subject = 'bug'
        subject = self.cleaned_data['Subject']
        message = self.cleaned_data['message']
        from_email = self.cleaned_data['email']
        recipient_list = [settings.EMAIL_HOST,]
        return send_mail(subject, message, from_email, recipient_list, fail_silently=False,)
