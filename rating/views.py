from django.http import HttpResponse
from django.template import loader

from blog.models import User


def index(request):
    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])

    print(user)
    userListNotModified = User.objects.all().order_by('-rating')
    template = loader.get_template('rating/index.html')
    userList=[]
    count=0
    class UserWithIndex:
        count=0

    for x in userListNotModified:
      #  print (x.username)
        count+=1
        temp = UserWithIndex()
        temp.count = count
        temp.obj=x
        userList.append(temp)

    context = {
        'userList': userList,
        'user': user,
    }
    return HttpResponse(template.render(context, request))