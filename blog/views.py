import bleach as bleach
import pycountry
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User as AuthUser

from project import settings
from .models import Blog, BlogComment, Comment, User, UserComment, UserBlog, BlogVote, CommentVote
from django.db import transaction

#helper functions
def updateBlogVotes(blogId, change, votingUser):
    blog = Blog.objects.get(id=blogId)
    blog.votes += change
    blog.save()
    print(blogId)
    blogUser = UserBlog.objects.get(blog_id=blogId).user
    print(blogUser.username, "jhev")
    blogUser.contribution += change
    blogUser.save()
    BlogVote(blog=blog, user=votingUser).save()

def updateCommentVotes(commentId, change, votingUser):
    comment = Comment.objects.get(id=commentId)
    comment.votes += change
    comment.save()
    commentUser = UserComment.objects.get(comment_id=commentId).user
    commentUser.contribution += change
    commentUser.save()
    CommentVote(comment=comment, user=votingUser).save()

def cleanMyField(myField):
    cleaned_text = bleach.clean(myField, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS,
                                settings.BLEACH_VALID_STYLES)
    return cleaned_text  # sanitize html

def canVoteBlog(user, blog):
    if BlogVote.objects.filter(blog=blog, user=user).exists():
        return False
    else:
        return True

def canVoteComment(user, comment):
    if CommentVote.objects.filter(comment=comment, user=user).exists():
        return False
    else:
        return True

def ownBlog(user, blog):
    return blog.user == user

def ownComment(user, comment):
    return comment.user == user

def returnAnyErrorBlog(user, blog):
    if user is None:
        return 'You should enter into the system before you vote'
    if ownBlog(user, blog):
        return 'You cannot vote for your blogs'
    if canVoteBlog(user, blog) == False:
        return 'You cannot vote twice. You have already voted for this topic before.'
    return None

def returnAnyErrorComment(user, comment):
    if user is None:
        return 'You should enter into the system before you vote'
    if ownComment(user, comment):
        return 'You cannot vote for your comments'
    if canVoteComment(user, comment) == False:
        return 'You cannot vote twice. You have already voted for this comment before.'
    return None



#helper functions


def index(request):
    user = None
    if 'memberId' in request.session:

        user = User.objects.get(id=request.session['memberId'])


    print(user)

    template = loader.get_template('blog/index.html')
    blogList = Blog.objects.all()

    class blogWithComments:
        noOfComments = 0

    blogWithCommentsList = []

    for blog in blogList:
        newObj = blogWithComments()
        newObj.blog = blog
        newObj.noOfComments = len(BlogComment.objects.filter(blog=blog))
        blogWithCommentsList.append(newObj)

    if request.POST:
        if "blogVote" in request.POST:
            change = 0
            blogId, type = [x for x in request.POST.get("blogVote").split(',')]
            currBlog = Blog.objects.get(id=blogId)

            popUpMessage = returnAnyErrorBlog(user, currBlog)

            if popUpMessage is None:
                if type == "up":
                    change = 1
                else:
                    change = -1
                updateBlogVotes(blogId, change, user)
                return HttpResponseRedirect("/blog/")
            else:
                context = {
                    'blogWithCommentsList': blogWithCommentsList,
                    'user': user,
                    'popUp': popUpMessage,
                }
                return HttpResponse(template.render(context, request))

    context = {
        'blogWithCommentsList': blogWithCommentsList,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


def blog(request, blogId):
    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])
    blog = Blog.objects.get(id=blogId)
    print(user)
    print(request.POST)

    commentList = BlogComment.objects.filter(blog_id=blogId)
    template = loader.get_template('blog/blog.html')
    if request.POST:
        if "blogVote" in request.POST:
            change = 0
            blogId, type = [x for x in request.POST.get("blogVote").split(',')]
            currBlog = Blog.objects.get(id=blogId)

            popUpMessage = returnAnyErrorBlog(user, currBlog)

            if popUpMessage is None:
                if type == "up":
                    change = 1
                else:
                    change = -1
                updateBlogVotes(blogId, change, user)
                return HttpResponseRedirect("/blog/{}".format(blogId))
            else:
                context = {
                    'blog': blog,
                    'commentList': commentList,
                    'noOfComments': len(commentList),
                    'user': user,
                    'popUp': popUpMessage,
                }
                return HttpResponse(template.render(context, request))

        elif "commentVote" in request.POST:
            change = 0
            commentId, type = [x for x in request.POST.get("commentVote").split(',')]
            currComment = Comment.objects.get(id=commentId)

            popUpMessage = returnAnyErrorComment(user, currComment)
            if popUpMessage is None:
                if type == "up":
                    change = 1
                else:
                    change = -1
                updateCommentVotes(commentId, change, user)
                return HttpResponseRedirect("/blog/{}".format(blogId))
            else:
                context = {
                    'blog': blog,
                    'commentList': commentList,
                    'noOfComments': len(commentList),
                    'user': user,
                    'popUp': popUpMessage,
                }
                return HttpResponse(template.render(context, request))

        elif "commentButton" in request.POST:
            buttonClicked = request.POST.get("commentButton")
            if buttonClicked == "post":
                description = request.POST.get("commentBox")
                description = cleanMyField(description)
                myComment = Comment(description=description, user=user, blog=blog)
                myComment.save()
                BlogComment(blog=blog, comment=myComment).save()
                UserComment(user=user, comment=myComment).save()
                return HttpResponseRedirect("/blog/{}/".format(blogId))

            else:
                return HttpResponseRedirect("/blog/{}/".format(blogId))



    context = {
        'blog': blog,
        'commentList': commentList,
        'noOfComments': len(commentList),
        'user': user,
    }
    return HttpResponse(template.render(context, request))



def new(request):
    user = None
    if 'memberId' in request.session:
        user = User.objects.get(id=request.session['memberId'])


    print(user)

    if request.POST:
        if "blogButton" in request.POST:
            buttonType = request.POST.get("blogButton")
            if buttonType == "post":
                print("hi")
                blogName = request.POST.get("blogName")
                blogName = cleanMyField(blogName)
                description = request.POST.get("blogDescription")
                description = cleanMyField(description)
                print(description)
                blog = Blog(blogName=blogName, user=user, description=description)
                blog.save()
                UserBlog(blog=blog, user=user).save()
                return HttpResponseRedirect("/blog/")
            else:
                return HttpResponseRedirect("/blog/")

    template = loader.get_template('blog/new.html')
    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))





#restrictive functions


class Construct:

    def constructBlog(self, blogId):  #and all its associated comments and users,doesnt do anything if already done
        response = requests.get('https://codeforces.com/api/blogEntry.view?blogEntryId={}'.format(blogId))
        blogObj = response.json()

        if blogObj['status'] == 'OK':
            username = blogObj['result']['authorHandle']
            blogName = blogObj['result']['title']
            description = blogObj['result']['content']
            blogUser = self.constructUser(username)
            blog = None
            if Blog.objects.filter(blogName=blogName).exists():
                blog = Blog.objects.get(blogName=blogName)
            else:
                blog = Blog(blogName=blogName, user=blogUser, description=description)
                blog.save()

            if UserBlog.objects.filter(user=blogUser, blog=blog).exists():
                pass
            else:
                UserBlog(user=blogUser, blog=blog).save()

            response2 = requests.get('https://codeforces.com/api/blogEntry.comments?blogEntryId={}'.format(blogId))
            commentObj = response2.json()

            if commentObj['status'] == 'OK':
                for comment in commentObj['result']:
                    commentDict = {}
                    username = comment['commentatorHandle']
                    description = comment['text']
                    commentDict['username'] = username
                    commentDict['description'] = description
                    self.constructComment(commentDict, blog)



    def constructComment(self, comment, blog):
        username = comment['username']
        description = comment['description']
        user = self.constructUser(username)

        myComment = Comment(user=user, description=description, blog=blog)
        myComment.save()

        if UserComment.objects.filter(user=user, comment=myComment).exists():
            pass
        else:
            UserComment(user=user, comment=myComment).save()

        if BlogComment.objects.filter(blog=blog, comment=myComment).exists():
            pass
        else:
            BlogComment(blog=blog, comment=myComment).save()




    def constructUser(self, username):
        password = '12345678'
        try:
            user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            AuthUser.objects.create_user(username=username, password=password)
            User(username=username, password=password).save()
            print("yes")

        return User.objects.get(username=username)








@transaction.atomic
def updateBlogDatabase1357(request, blogId): #updates the database with this blogId
    createBlog = Construct()
    createBlog.constructBlog(blogId)
    return HttpResponse("Done")


def updateUserDatabase1357(request): #updates the database with this blogId
    userList = User.objects.all()

    for user in userList:
        response = requests.get('https://codeforces.com/api/user.info?handles={}'.format(user.username))
        userObj = response.json()

        if userObj['status'] == 'OK':
            firstName = ""
            lastName = ""
            if "firstName" in userObj["result"][0]:
                firstName = userObj["result"][0]["firstName"]
            if "lastName" in userObj["result"][0]:
                lastName = userObj["result"][0]["lastName"]

            name = "{} {}".format(firstName, lastName)

            countryName = ""
            if "country" in userObj["result"][0]:
                countryName = userObj["result"][0]["country"]

            contribution = 0
            if "contribution" in userObj["result"][0]:
                contribution = userObj["result"][0]["contribution"]

            rating = 1400
            if "rating" in userObj["result"][0]:
                rating = userObj["result"][0]["rating"]

            profilePhoto = userObj["result"][0]["avatar"]


            user.name = name
            try:
                code = pycountry.countries.get(name=countryName).alpha_3
                user.country = code
            except AttributeError:
                user.country = ""
            user.contribution = contribution
            user.rating = rating
            user.profilePhoto = profilePhoto
            user.save()


    return HttpResponse("Done")




#restrictive functions
