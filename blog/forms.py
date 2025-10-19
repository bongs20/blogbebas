from django import forms
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Category, UserProfile, Tag


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels (ID)
        self.fields['username'].label = 'Nama pengguna'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Kata sandi'
        self.fields['password2'].label = 'Ulangi kata sandi'
        # Placeholders & classes
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nama pengguna',
            'autocomplete': 'username',
            'autofocus': 'autofocus',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Kata sandi',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ulangi kata sandi',
            'autocomplete': 'new-password',
        })


class PostForm(forms.ModelForm):
    attachment = forms.FileField(required=False)
    attachment_url = forms.URLField(required=False)
    tags = forms.CharField(required=False, help_text='Comma-separated tags')
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control markdown-input', 'rows': 8, 'placeholder': 'Tulis konten dengan Markdown...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit categories to top 20 or search by query 'q'
        field = self.fields.get('category')
        if isinstance(field, forms.ModelChoiceField):
            base = Category.objects.all().order_by('name')
            q = None
            if getattr(self, 'data', None):
                q = self.data.get('q') or None
            qs = base.filter(name__icontains=q) if q else base
            # Build a list of IDs to avoid distinct() with sliced queryset
            ids = list(qs.values_list('pk', flat=True)[:20])
            # Always include the selected category id (from POST or instance)
            selected_id = None
            if getattr(self, 'data', None):
                cat_val = self.data.get('category')
                if cat_val:
                    try:
                        selected_id = int(cat_val)
                    except Exception:
                        selected_id = None
            if not selected_id and getattr(self.instance, 'category_id', None):
                selected_id = self.instance.category_id
            if selected_id and selected_id not in ids:
                ids.append(selected_id)
            field.queryset = Category.objects.filter(pk__in=ids).order_by('name')

    def clean(self):
        cleaned = super().clean()
        # Normalize URL field
        url = cleaned.get('attachment_url')
        if url is not None and isinstance(url, str):
            cleaned['attachment_url'] = url.strip()
        # normalize tags
        t = (self.data.get('tags') or '').strip() if getattr(self, 'data', None) else ''
        cleaned['tags'] = ','.join([s.strip() for s in t.split(',') if s.strip()]) if t else ''
        return cleaned

    # No approval gating; anyone can select any category


class CommentForm(forms.ModelForm):
    attachment = forms.FileField(required=False)
    attachment_url = forms.URLField(required=False)
    class Meta:
        model = Comment
        fields = ['content']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deskripsi komunitas'}),
        }

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get('name')
        slug = cleaned.get('slug')
        if name and not slug:
            cleaned['slug'] = slugify(name)
        elif slug:
            cleaned['slug'] = slugify(slug)
        return cleaned


class CommunitySearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cari komunitas...'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'bio', 'avatar']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
