from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import stripe
import uuid

#a product create call will be made when user is switched to celeb, pass in the user
class Product(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=80, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        self.name = self.user.username + ' FanMoji Account '
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
    celeb = models.ManyToManyField(User, related_name='Celeb')
    stripe_id = models.CharField(max_length=80, default='')
    fan = models.ManyToManyField(User, related_name='Fan')
    cancelled = models.BooleanField(default=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#this will be the primary key

    def save(self, *args, **kwargs):
        if self.cancelled == True: #or self.userTo in self.userFrom.profile.following: #and user saving it is the userTo:
            user = User.objects.get(username=celeb.username)
            request.user.profile.following.remove(user)
            return None
        else:
            super(AccountRequest, self).save(*args, **kwargs)

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
