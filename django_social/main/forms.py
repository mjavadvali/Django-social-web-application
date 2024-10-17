from django import forms
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title' ,'content', 'photo', 'tagged_users']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-input', 'placeholder': 'enter the title of your post ...'})
        self.fields['content'].widget.attrs.update({'class': 'form-input', 'placeholder': 'type the content of your post ...'})
        self.fields['photo'].widget.attrs.update({'class': 'photo-form'})
        
        self.user = kwargs.pop('user', None)

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment        

        fields = ['content', 'parent']
        
        labels = {
            'content': _(''),
        }
        
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'comment-input',
                'placeholder': 'Comment ...',
            }),
            'parent': forms.Select(attrs={
                'class': 'reply-input-choices',  
            }),
        }
    
    def __init__(self, *args, **kwargs):
        post = kwargs.pop('post', None)
        
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'comment-input', 
            'placeholder': 'comment ...'
        })
        if post:
            self.fields['parent'].queryset = Comment.objects.filter(post=post)
            
    