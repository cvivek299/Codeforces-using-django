from django.db import models
from django_countries.fields import CountryField
# Create your models here.
#default null,blank->false  null for database(empty allowed or not),similarly blank for form

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(default="",max_length=50, null=True, blank=True)
    country = CountryField(default="", null=True, blank=True)
    contribution = models.IntegerField(default=0, null=True, blank=True)
    rating = models.IntegerField(default=1400, null=True, blank=True)
    profilePhoto = models.ImageField(default="https://userpic.codeforces.com/no-avatar.jpg", blank=True, null=True,   #optional in both form and db
                                     upload_to="profilePhoto/%Y/%m/%D/")

    def __str__(self):
        return "{} ({})".format(self.name, self.username)

class Blog(models.Model):
    blogName = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=6000, default="")
    votes = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.blogName)

class Comment(models.Model):
    description = models.CharField(max_length=500, default="")
    votes = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class UserBlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "blog"),)

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("blog", "comment"),)

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "comment"),)
