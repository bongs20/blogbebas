from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_categories')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    icon = models.FileField(upload_to='communities/icons/', blank=True, null=True)
    moderators = models.ManyToManyField(User, related_name='moderated_communities', blank=True)

    class Meta:
        verbose_name = 'Komunitas'
        verbose_name_plural = 'Komunitas'

    def __str__(self):
        return self.name or self.slug

    # Permission helpers
    def is_owner(self, user: User) -> bool:
        return bool(user and user.is_authenticated and (user == self.created_by or user.is_superuser))

    def can_moderate(self, user: User) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if user == self.created_by:
            return True
        return self.moderators.filter(pk=user.pk).exists()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # Moderation
    is_pinned = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    comments_locked = models.BooleanField(default=False)
    # Tags for post (per community)
    # Declared after Tag class; use string reference to 'Tag'.
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def score(self):
        # Backward-compatible method; prefer net_score property.
        # Use explicit query to satisfy static analyzers.
        total = Vote.objects.filter(post=self).aggregate(total=Sum('value'))['total']
        return total or 0

    @property
    def net_score(self):
        total = Vote.objects.filter(post=self).aggregate(total=Sum('value'))['total']
        return total or 0

    def __str__(self):
        return self.title


class Tag(models.Model):
    community = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60)

    class Meta:
        unique_together = ('community', 'slug')

    def __str__(self):
        return f'{self.community.slug}:{self.name}'


# (tags field declared on Post via string reference)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user} -> {self.post} : {self.value}'


class PostAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/', blank=True, null=True)
    url = models.URLField(blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        name = self.file.name if self.file else self.url
        return f'Attachment for {self.post.pk}: {name}'


class CommentAttachment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/', blank=True, null=True)
    url = models.URLField(blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        name = self.file.name if self.file else self.url
        return f'Attachment for comment {self.comment.pk}: {name}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    # Admin-assignable badges
    active_badge = models.BooleanField(default=False, help_text='Grant ability to create komunitas without upvotes requirement')
    custom_badge_label = models.CharField(max_length=30, blank=True, help_text='Optional custom badge label to display on profile')
    custom_badge_style = models.CharField(max_length=20, blank=True, help_text='Bootstrap color: primary/success/info/warning/danger/secondary')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Profile({self.user.username})'


class CommunityMember(models.Model):
    ROLE_MEMBER = 'member'
    ROLE_CHOICES = (
        (ROLE_MEMBER, 'Member'),
    )
    community = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_memberships')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('community', 'user')

    def __str__(self):
        return f'{self.user.username} in r/{self.community.slug}'


# (helper methods are defined on Category class)
