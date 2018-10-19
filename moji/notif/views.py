from django.shortcuts import render
from .models import Notfication
from .forms import NotficationForm

def editNotif(request):
    if request.method  == "POST":
        form = NotficationForm(request.POST, instance=request.user.notification)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.new_sub = form.cleaned_data['new_sub']
            notif.re_subbed = form.cleaned_data['re_subbed']
            notif.like = form.cleaned_data['like']
            notif.points_add = form.cleaned_data['points_add']
            notif.points_spent = form.cleaned_data['points_spent']
            notif.transctions = form.cleaned_data['transctions']
            notif.tip = form.cleaned_data['tip']
            notif.save()
            return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
    else:
        form = NotficationForm(instance=request.user.notification)
        return render(request, 'pages/6/edit.html', {'form':form})

def sendNotif(action, x, y):
    send_mail(
        'action',
        'Congrats on the new' + x,
        'from@example.com',
        [y.email],
        fail_silently=False,
    )

'''
def IsNotif(x, y):
    if request.user.notification.action == True:
        sendNotif(x, y)
    else:
        None
'''
