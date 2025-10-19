from django.contrib import admin
from .models import Post, Comment, Vote, Category, PostAttachment, CommentAttachment, Tag, UserProfile

# Admin branding
admin.site.site_header = 'BlogBebas Administration'
admin.site.site_title = 'BlogBebas Admin'
admin.site.index_title = 'Manage BlogBebas'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_pinned', 'is_removed', 'comments_locked', 'created_at')
    list_filter = ('category', 'author', 'is_pinned', 'is_removed', 'comments_locked')
    search_fields = ('title', 'content')
from .models import Post, Comment, Vote, Category, PostAttachment, CommentAttachment, Tag, UserProfile, CommunityMember


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
    mark_verified.short_description = 'Tandai terverifikasi'

    def mark_unverified(self, request, queryset):
        queryset.update(is_verified=False)
    mark_unverified.short_description = 'Batalkan verifikasi'


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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'active_badge', 'custom_badge_label', 'custom_badge_style', 'created_at')
    search_fields = ('user__username', 'display_name', 'custom_badge_label')
    list_filter = ('active_badge',)
    actions = ['grant_active', 'revoke_active']

    def grant_active(self, request, queryset):
        queryset.update(active_badge=True)
    grant_active.short_description = 'Beri badge Active'

    def revoke_active(self, request, queryset):
        queryset.update(active_badge=False)
    revoke_active.short_description = 'Cabut badge Active'


@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ('community', 'user', 'role', 'joined_at')
    list_filter = ('role', 'community')
    search_fields = ('community__name', 'community__slug', 'user__username')
