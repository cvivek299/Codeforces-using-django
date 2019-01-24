import bleach
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from blog.models import User
from django.contrib.auth.models import User as AuthUser

#helper functions
from project import settings


def cleanMyField(myField):
    cleaned_text = bleach.clean(myField, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS,
                                settings.BLEACH_VALID_STYLES)
    return cleaned_text  # sanitize html

#helper functions

def login(request):
    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])

    if user:
        return HttpResponseRedirect('/userprofile/{}'.format(user.username))

    print(request.POST)
    template = loader.get_template('entry/login.html')
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None: #valid user, so login,and redirect to blog page
            #set session of this user (memberId to his id)
            print("yes")
            userObj = User.objects.get(username=username)
            request.session['memberId'] = userObj.id
            return HttpResponseRedirect("/blog")
        else:#invalid user so same page
            context = {
                'user': user,
                'error': 'Invalid handle or password',
            }
            return HttpResponse(template.render(context, request))


    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))

def logout(request):
    try:
        del request.session['memberId']
    except KeyError:
        pass

    return HttpResponseRedirect("/blog")

def register(request):
    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])

    if user:
        return HttpResponseRedirect('/userprofile/{}'.format(user.username))

    print(request.POST)
    template = loader.get_template('entry/register.html')
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        samePassword = request.POST.get("confirmPassword")
        if password == samePassword:
            try:
                AuthUser.objects.get(username=username)
                context = {
                    'user': user,
                    'handleError': 'This handle is currently in use',
                }
                print("no")
                return HttpResponse(template.render(context, request))

            except AuthUser.DoesNotExist:
                username = cleanMyField(username)
                AuthUser.objects.create_user(username=username, password=password)
                User(username=username, password=password).save()
                print("yes")
                return HttpResponseRedirect("/blog")
        else:
            context = {
                'user': user,
                'passwordError': 'Confirmation mismatched',
            }
            print("no")
            return HttpResponse(template.render(context, request))


    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))


