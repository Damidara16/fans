from django.shortcuts import render, redirect
from account.models import Profile, AccountRequest
from content.models import Content
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from .forms import RegistrationForm, EditProfileForm, UpdateUserForm, RequestForm
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View

#ACCOUNT SUITE

def blockUser(request, uuid=None):
    try:
        user = User.objects.get(uuid=uuid)
    except User.DoesNotExist():
        raise Http404("User does not exist")
    if user == request.user:
        return None
        return redirect(reverse('home:home'))
    elif user in request.user.profile.following:
        request.user.profile.following.remove(user)
        request.user.followed_by.remove(user)
        request.user.profile.blocked.add(user)
        return redirect(reverse('home:home'))
    else:
        request.user.profile.blocked.add(user)
        return redirect(reverse('home:home'))
    #take the user and current user,
    #1. blocked the user by adding to blocked list
    #2. remove user from following

def unblockUser(request, uuid=None):
    try:
        user = User.objects.get(uuid=uuid)
    except User.DoesNotExist():
        raise Http404("User does not exist")
    request.user.profile.blocked.remove(user)
    return redirect(reverse('home:home'))

def ViewProfile(request, name=None):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if name == request.user.username:
        return render(request, "pages/1/ownerprofile.html", {"user":user})
    elif user.profile.private and user not in request.user.profile.following.all():
        return render(request, "pages/1/privateprofile.html", {"user":user})
    else:
        return render(request, "pages/1/viewprofile.html", {"user":user})

def updateProfile(request):
    if request.method  == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        form1 = UpdateUserForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and form1.is_valid():
            #profile = form.save(commit=False)
            #profile.first_name = form.cleaned_data['first_name']
            #profile.last_name = form.cleaned_data['last_name']
            #profile.email = form.cleaned_data['email']
            form.save()
            form1.save()
            return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
        else:
            #messages.error(request, "Error")
            return render(request, 'pages/2/signup.html', {'form':form})

    else:
        form = EditProfileForm(instance=request.user)
        form1 = UpdateUserForm(instance=request.user.profile)
        return render(request, 'pages/5/editprofile.html', {'form':form, 'form1':form1})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            '''reg = form.save(commit=False)
            reg.email = form.cleaned_data['email']
            reg.username = form.cleaned_data['username']
            reg.first_name = form.cleaned_data['first_name']
            reg.last_name = form.cleaned_data['last_name']
            reg.password1 = form.cleaned_data['password1']
            reg.password2 = form.cleaned_data['password2']

            reg.save()'''
            return redirect(reverse('account:login'))

        else:
            #messages.error(request, "Error")
            return render(request, 'pages/2/signup.html', {'form':form})

    else:
        form = RegistrationForm()
        return render(request, 'pages/2/signup.html', {'form':form})

def deleteProfile(request):
    #add a re-enter passcode to delete account
    user = User.objects.get(uuid=request.user.uuid)
    user.delete()
    return redirect('/home')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('content:CreatePost'))
        else:
            return redirect(reverse('account:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'account/password.html', args)


#PREVIEW SUITE
'''method 1, on content list a add to preview link is there and sends the id of the content to this url and adds as a preview,
and vise versa when they want to remove.
'''

def previewRemoveAdd(request, uuid=None):
    #print(str(uuid))
    try:
        content = Content.objects.get(uuid=uuid)
    except User.DoesNotExist():
        raise Http404("User does not exist")
    if content.user == request.user and content.preview == False:
        content.preview = True
        content.save()
        return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
    elif content.user == request.user and content.preview == True:
        content.preview = False
        content.save()
        return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
    else:
        return redirect(reverse('home:home'))




#FOLLOW SUITE

def listRequests(request):
    return render(request, 'pages/lists/requestlist.html')

def detailRequests(request, name):
    try:
        user = User.objects.get(username=name)
        req = request.user.requested.get(userFrom=user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    return render(request, 'account/reqDetail.html', {'req':req})

def deleteRequests(request, name):
    try:
        user = User.objects.get(username=name)
        req = request.user.requested.get(userFrom=user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
        req.delete()
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def editRequests(request, name):
    try:
        user = User.objects.get(username=name)
        req = request.user.requested.get(userFrom=user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
        req.accept = True
        req.save()
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def makeRequests(request, name):
    #need to add where one model can be made, probably use the sent field
    try:
        user = User.objects.get(username=name)
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    if AccountRequest.objects.filter(userFrom=request.user).get(userTo=user).exists():
        return None
    else:
        accept = AccountRequest()
        accept.userTo = user
        accept.userFrom = request.user
        accept.save()
        return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def unfollowUser(request, name):
    try:
        user = User.objects.get(username=name)
        request.user.profile.following.remove(user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that user")
    return redirect(reverse('home:home'))
