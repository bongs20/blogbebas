from django.contrib import admin
from .models import Post, Comment, Vote, Category, PostAttachment, CommentAttachment, Tag

# Admin branding
admin.site.site_header = 'BlogBebas Administration'
admin.site.site_title = 'BlogBebas Admin'
admin.site.index_title = 'Manage BlogBebas'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'author')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_verified', 'created_by', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('moderators',)
    actions = ['mark_verified', 'mark_unverified']

    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)
    mark_verified.short_description = 'Mark selected categories as verified'

    def mark_unverified(self, request, queryset):
        queryset.update(is_verified=False)
    mark_unverified.short_description = 'Mark selected categories as unverified'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'value')


@admin.register(PostAttachment)
class PostAttachmentAdmin(admin.ModelAdmin):
    list_display = ('post', 'file', 'url', 'content_type', 'created_at')


@admin.register(CommentAttachment)
class CommentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'file', 'url', 'content_type', 'created_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'community')
    search_fields = ('name', 'slug', 'community__name', 'community__slug')
    list_filter = ('community',)
