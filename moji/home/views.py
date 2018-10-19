from django.shortcuts import render, redirect, Http404
from content.models import Content, Comment, Like
from account.models import Profile
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import Reporter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def index(request):
    if request.user.is_authenticated():
        followers = request.user.profile.following.all()
        #THIS WOULD ADD THE CURRENT USERS POST TO THE HOME PAGE
        #a = []
        #for i in followers:
        #    a.append(i)
        #a.append(request.user)
        #ADD REQUEST.USER TO THEIR OWN FOLLOWING
        queryset_list = Content.objects.filter(user__in=followers).order_by('-date')
        pagenated_query = Paginator(queryset_list, 25)
        #use .object_list to access the item in paginator
        page = request.GET.get('page')
        try:
            if page != None and int(page) > pagenated_query.num_pages:
                following_query = pagenated_query.page(pagenated_query.num_pages)
            else:
                following_query = pagenated_query.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            following_query = pagenated_query.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            following_query = pagenated_query.page(paginator.num_pages)

            #check the django doc for use in templates
        return render(request, 'pages/1/homeAuth.html', {'following_query':following_query})
    else:
        return render(request, 'pages/1/homeunAuth.html')

def SearchUser(request):
    query = request.GET.get('q')
    if query:
        queryset_list = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(location__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
        ).distinct().exclude(user=request.user)[:16]
        print(queryset_list)
        return render(request, 'pages/7/searched.html', {'queryset_list':queryset_list})
    else:
        return None

def discoverView(request):
    page = 'Spotlight'
    users = User.objects.order_by('?')[:24]
    return render(request, 'pages/7/discover.html', {'users':users, 'page':page})

def discoverGenre(request, genre):
    page = genre
    try:
        users = Profile.objects.filter(genre_exact=genre).filter('?')[:24]
    except Profile.DoesNotExist:
        raise http404('cant find any users under this genre')
    return render(request, 'pages/7/discover.html', {'users':users, 'page':page})

def aboutUs(request):
    return render(request, 'pages/2/about.html')

def Hww(request):
    return render(request, 'pages/2/hww.html')

class emailReport(FormView):
    template_name = 'home/contact.html'
    form_class = Reporter
    success_url = '/home/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(emailReport, self).form_valid(form)


'''
class BugReport(emailReport):
    we dont need their email
    user makes the message, subject is always bug
    pass

class ViolationReport(emailReport):
    we dont need their email
    should just be choice:
    ex.
    illegal content
    slander
    bullying
    offensive
    missed advertised
    aggresive or endangering of human/animal
    copyright
    and then grabs a screenshot of the violation
    pass

class ContactReport(emailReport):
    user makes subject and message
    we need their email
    this is for potential users or celebs
    pass

class SupportReport(emailReport):
    user makes subject and message, and the users account
    we need their email
    this is for paid users, about their account or using the service
    pass
'''
