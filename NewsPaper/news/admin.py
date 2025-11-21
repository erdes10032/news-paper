from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

def nullfy_rating(modeladmin, request, queryset):
    queryset.update(post_rating=0)
nullfy_rating.short_description = 'Nullfy rating'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'post_type', 'good_rating')
    list_filter = ('post_type', 'post_rating')
    search_fields = ('title', 'text')
    actions = [nullfy_rating]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'comment_rating')
    list_filter = ('user', 'comment_rating')
    search_fields = ['text']

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)