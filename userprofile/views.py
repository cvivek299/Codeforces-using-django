import json

import pycountry
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django_countries.fields import Country


from blog.models import User, UserBlog


def index(request, username):
    print(username)
    profileUser = None
    try:
        profileUser = User.objects.get(username=username)
    except User.DoesNotExist:
        pass

    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])

    noOfBlogs = 0
    if profileUser:
        noOfBlogs = len(UserBlog.objects.filter(user=profileUser))

    template = loader.get_template('userprofile/index.html')

    context = {
        'user': user,
        'noOfBlogs': noOfBlogs,
        'profileUser': profileUser,
    }
    return HttpResponse(template.render(context, request))

def social(request):

    json_data = open('C:/Users/cs160/OneDrive/Desktop/project/userprofile/templates/userprofile/country-by-name.json').read()

    jsonData2 = json.dumps(json_data)  # converts to a json structure

    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])

    if request.POST:
        name = request.POST.get("Name")
        country = request.POST.get("Country")

        try:
            code = pycountry.countries.get(name=country).alpha_3
            user.name = name
            user.country = code
            user.save()
            return HttpResponseRedirect("/userprofile/{}".format(user.username))
        except AttributeError:
            return HttpResponseRedirect("#")


    template = loader.get_template('userprofile/social.html')
    context = {
        'user': user,
        'jsonData2': jsonData2,
    }
    return HttpResponse(template.render(context, request))

