from django.shortcuts import render
from .models import Tip, PointsWallet, Points, Plan
from banking.models import TransactionHistory
from django.contrib.auth.models import User
from .forms import SetPoint
from account.models import Profile
from django.views.generic.edit import CreateView, UpdateView
import stripe

def viewStripe(request):
    account = stripe.Account.retrieve("{CONNECTED_STRIPE_ACCOUNT_ID}")
    a = account.login_links.create()
    stripeurl = a['url']
    return render(request, 'pages/5/viewstripe.html', {'stripeurl':stripeurl})
#CRUD PLAN
#HANDLES MAKING A NEW PLAN, UPDATING AN EXISTING, AND DELETING A CURRENT PLAN
#grandfather plans could work by presenting the newest plan, but old plans are still chargable but not accessable
class CreatePlan(CreateView):
    model = Plan
    fields = ['price', 'description']
    template_name = 'content/make.html'
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePlan, self).form_valid(form)


class PointsUpdate(UpdateView):
    model = Points
    fields = ['like', 'comment']
    template_name_suffix = 'content/make.html'

#CRUD SUBSCRIPTION
#HANDLES A USER PAYING FOR A SUBSCRIPTION, RETRIEVE SUBSCRIPTION, AND CANCELLING A SUBSCRIPTION
#this is a button view
def tempSub(request, uuid):
    celeb = Profile.objects.get(uuid=uuid)
    return render(request, 'pages/5/tempsub.html', {'celeb':celeb.user.plan_set.all().last()})

def addSub(request, uuid):
    celeb = Profile.objects.get(uuid=uuid)
    a = stripe.Subscription.create(
    customer = request.user.stripe_customer.stripe_id,
    # -1 for the latest one
    plan = celeb.plan_set.filter().last(),
    application_fee_percent=celeb.profile.percentage,
    stripe_account = celeb.stripe_account.stripe_id
    )
    if a['status'] == 'success':
        request.user.following.add(celeb)
        TransactionHistory.objects.create(fan=request.user, celeb=celeb.user, transctionType='Subscription', amount=celeb.user.plan_set.all().last().price)
        return render(request, 'pages/5/success/html',)

    else:
        error = {'code':a['status'], 'reason':a['outcome']['reason']}
        return render(request, 'pages/5/success/html', {'error':error})
#this is button view
def cancelSub(request, user):
    celeb = User.objects.get(username=user)
    #point = TransactionHistory.objects.filter(fan=request.user).get(celeb=user)
    retrievedSub = request.user.TransactionHistory.filter(transctionType='Subscription').get(celeb=user)
    sub = stripe.Subscription.retrieve(retrievedSub.transction_id, stripe_account=celeb.ConnectStripeAccount.stripe_id)
    sub.at_period_end = true
    return redirect(reverse('home:home'))

#MIDDLEWARE EXEMPT, not secure
#webhook
def removeUser(request):
    ree = request.GET.get('key')
    celeb = request.GET.get('name')
    if ree == 'irfew234ffm430fm2':
        user = User.objects.get(username=name)
        request.user.profile.following.remove(user)
        return None
    else:
        return None

#CRUD TIP
def SendTip(request, user=None):
    if request.method  == "POST":
        form = MakeTip(request.POST)
        if form.is_valid():
            try:
                stripe.api_key = settings.STRIPE_KEY
                cel = User.objects.get(username=user)
                account = stripe.Account.retrieve(cel.ConnectStripeAccount.stripe_id)

                token = stripe.Token.create(
                  customer=request.user.customer.stripe_id,
                  stripe_account= account.id
                )

                #tip will be the amount given by the fan
                tip = form.cleaned_data['amount']

                charge = stripe.Charge.create(
                  amount=tip,
                  currency="usd",
                  description= form.cleaned_data['description'],
                  source = token.id,
                  application_fee= int((tip * cel.profile.percentage)),
                  stripe_account=account.id,
                  metadata = {'celeb':user.username, 'fan':request.user.username, 'tip':'tip'}
                )
                if charge['status'] == 'success':
                    profile = form.save(commit=False)
                    profile.celeb = user
                    profile.transctionType = 'Tip'
                    profile.fan = request.user
                    profile.description = form.cleaned_data['description']
                    profile.amount = form.cleaned_data['amount']
                    profile.transction_id = str(charge.id)
                    profile.save()

            except charge['status'] != 'success':
                error = {'code':a['status'], 'reason':a['outcome']['reason']}
                return render(request, 'pages/5/success/html', {'error':error})
                #send message to tipped and save in TransactionHistory
                #should redirect to a success page or pass back a success param
            return render(request, 'pages/5/success/html',)
    else:
        form = MakeTip()
        return render(request, 'pages/5/sendtip.html', {'form':form})

#CRUD REWARDS + claim reward

def SetPoints(request):
    if request.method  == "POST":
        form = SetPoint(request.POST, instance=request.user.points)
        if form.is_valid():
            point = form.save(commit=False)
            point.likes = form.cleaned_data['likes']
            point.comment = form.cleaned_data['comment']
            point.save()
            return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
    else:
        form = SetPoint(instance=request.user.points)
        return render(request, 'account/update.html', {'form':form})
