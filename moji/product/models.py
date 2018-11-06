from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import stripe
import uuid

class Coupons(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    max_redemptions = models.PositiveIntegerField(null=True, default=10000)# default set 10,000 incase user leave blank, thus meaning unlimited uses
    #time_limit = models.PositiveIntegerField(null=True, default=0)

    def save(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_KEY
        if self.percent_off <= 100.00:
            self.percent_off = 100.00
        stripe.Coupon.create(
          id = self.name,
          stripe_account = self.user.ConnectStripeAccount.stripe_id,
          percent_off = self.percent_off,
          duration = 'once',
          max_redemptions = self.max_redemptions
        )
        return super(Coupons, self).save(*args, **kwargs)

#a product create call will be made when user is switched to celeb, pass in the user
class Product(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=80, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        self.name = self.user.username + ' FanMojis Account '
        stripe.api_key = settings.STRIPE_KEY

        a = stripe.Product.create(
          name= self.name + 'subscription plan',
          type='service',
        )
        self.stripe_id = a['id']
        return super(Product, self).save(*args, **kwargs)


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255)
    nickname = models.CharField(max_length=105)
    stripe_id = models.CharField(max_length=80, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#this will be the primary key

#make sure price matches with django numbers
    def __str__():
        return self.nickname


    def save(self, *args, **kwargs):
        self.nickname = self.user.username + str(self.price) + 'plan'
        a = stripe.Plan.create(
          nickname=self.nickname,
          product=self.user.product.stripe_id,
          amount= self.price,
          currency="usd",
          interval="month",
          stripe_account = self.user.ConnectStripeAccount.stripe_id
        )
        self.stripe_id = a['id']
        return super(Plan, self).save(*args, **kwargs)

class Subscription(models.Model):
    types = (('Bundle', 'Bundle'),('Single', 'Single'))
    celeb = models.ManyToManyField(User, related_name='Celeb')
    stripe_id = models.CharField(max_length=80, default='')
    fan = models.ManyToManyField(User, related_name='Fan')
    cancelled = models.BooleanField(default=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#this will be the primary key
    linked = models.ManyToManyField('self', null=True)
    type = models.CharField(choices=types, max_length=50)

    def save(self, *args, **kwargs):
        if self.type == 'Bundle':
            self.fan.profile.following.remove(self.linked.celeb)
        if self.cancelled == True: #or self.userTo in self.userFrom.profile.following: #and user saving it is the userTo:
            #user = User.objects.get(username=self.celeb.username)
            self.fan.profile.following.remove(self.celeb)
            return None
        else:
            super(Subscription, self).save(*args, **kwargs)


class BundlePlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255)
    nickname = models.CharField(max_length=105)
    stripe_id = models.CharField(max_length=80, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#this will be the primary key
    bundled = models.BooleanField(default=False)
    linked = models.OneToOneField('self', null=True)
    bundledWith = model.ForeignKey(User, on_delete=models.CASCADE, related_name='celebBundledWith')
#TWO USERS CREATE A PLAN AND USING THE LINKED FIELD THEIR LINKED TOGETHER.
#MAKES A SUBSCRIPTION CALL TO ONE BUNDLE AND CREATE ONE FOR THE OTHER
#WHEN A FAN WANTS TO BUY A BUNDLE, DJANGO GETS BUNDLE AND CREATES A SEPERATE SUBSCRIPTION TO BOTH PLANS
#WHEN A FAN WANTS TO CANCEL THE PLAN, DJANGO WILL GET ONE PLAN AND END BOTH PLANS

#make sure price matches with django numbers
    def __str__():
        return self.nickname


    def save(self, *args, **kwargs):
        self.nickname = self.user.username + str(self.price) + 'plan'
        a = stripe.Plan.create(
          nickname=self.nickname,
          product=self.user.product.stripe_id,
          amount= self.price,
          currency="usd",
          interval="month",
          stripe_account = self.user.ConnectStripeAccount.stripe_id
        )
        self.stripe_id = a['id']
        BundlePlanRequest.objects.create(celebSender=request.user, celebReceiver=self.bundledWith, bundle=self)#there my be an error with just using self
        return super(Plan, self).save(*args, **kwargs)

class BundlePlanRequest(models.Model):
    celebSender = models.ForeignKey(User, related_name='requester')
    celebReceiver = models.ForeignKey(User, related_name='requested')
    bundle = models.OneToOneField(BundlePlan)
    #user.requested.all() -> gives all the Requested invites and vise-versa
    accept = models.BooleanField(default=False)
    sent = models.BooleanField(default=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.userTo.username

    def get_absolute_url(self):
        return reverse('account:detailAcceptance', kwargs={'name':self.userTo.username})

    def save(self, *args, **kwargs):
        if self.userFrom.profile in self.userTo.followed_by.all():
            return None
        elif self.accept == True: #or self.userTo in self.userFrom.profile.following: #and user saving it is the userTo:
            BundlePlan.objects.create(linked=self.bundle, bundledWith=self.celebSender)
            #the user provides the description, price, and nickname, when user save their plan change bundled to True
            self.delete()
            return None
        else:
            super(AccountRequest, self).save(*args, **kwargs)
 #CREATE A SIGNAL THAT DELETES THE PLAN IF REQUEST IS DENIED or some shit like
'''
def MakePlan(sender, **kwargs):
    if kwargs['created']:
        #make api call to stripe and make actual plan
        pass

post_save.connect(MakePlan, sender=Plan)
'''

class Points(models.Model):
    #each user is assigned a point model
    #and when a fan does an action, a view will reference the celeb point model add that value
    #based on the model.
    #points are added to a fan-celeb 'bank account' which can only be access by the fan
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #this will be the primary key
    user = models.OneToOneField(User)
    likes = models.PositiveIntegerField(default=0)
    comment = models.PositiveIntegerField(default=0)
    #have a view that adds and subtrack points based on the operation
    def __str__(self):
        return self.user.username

class PointsWallet(models.Model):
    #add a post save signal that creates a pointswallet when users add each other
    walletname = models.CharField(max_length=115)
    user = models.ForeignKey(User)
    amount = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    def __str__(self):
        return self.user.username + ' Points Wallet with ' + self.walletname

class Tip(models.Model):
    tipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Donor')
    tipped = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Donated')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    reason = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

'''
class Reward(models.Model):
    #so celeb sets reward, fan claims reward,
    #1.points are reduced, 2.email sent to celeb and fan, 3.if reward is any of the choice. Our system will automatically do the action
    #4.if it is custom then the celeb will sent the email saying to follow through on the reward and our system will track the process
    Prizes = (('discount','D'), ('first access', 'FA'), ('real item', 'RI'), ('custom', 'C'))
    cost = models.PositiveIntegerField(default=0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #remdeemer = models.ForeignKey(User)
    prize = models.CharField(max_length=10, choices=Prizes)
    description = models.CharField(max_length=255)
'''
