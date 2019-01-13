from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from blog.models import User
from django.contrib.auth.models import User as AuthUser


def login(request):
    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])

    print(request.POST)
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
            print("no")
            return HttpResponseRedirect("#")

    template = loader.get_template('entry/login.html')
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

    print(request.POST)
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        samePassword = request.POST.get("confirmPassword")
        if password == samePassword:
            try:
                user = AuthUser.objects.get(username=username)
                print("no")
                return HttpResponseRedirect("#")
            except AuthUser.DoesNotExist:
                AuthUser.objects.create_user(username=username, password=password)
                User(username=username, password=password).save()
                print("yes")
                return HttpResponseRedirect("/blog")
        else:
            print("no")
            return HttpResponseRedirect("#")

    template = loader.get_template('entry/register.html')
    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))


