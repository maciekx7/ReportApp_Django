from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Post, Comment

# Register your models here.
admin.site.register(Post, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
