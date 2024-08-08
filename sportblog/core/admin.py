from django.contrib import admin
from . import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'publish', 'category')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at', 'updated_at')

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'content', 'created_at', 'updated_at')

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Reply, ReplyAdmin)
admin.site.register(models.Category, CategoryAdmin)