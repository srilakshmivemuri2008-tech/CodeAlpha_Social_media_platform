from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Post, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bio', 'avatar_url')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'maxlength': 300, 'placeholder': 'Tell people about yourself...'}),
            'avatar_url': forms.URLInput(attrs={'placeholder': 'https://example.com/your-photo.jpg'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image_url')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Optional image link'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Write a comment...'}),
        }
