from django.contrib import admin
from .models import User, Blog, Comment, BlogComment, UserBlog, UserComment

# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(BlogComment)
admin.site.register(UserBlog)
admin.site.register(UserComment)
