from django import forms
from django.forms import formset_factory

from forumapp.models import Post, Comment


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

class PostCreateForm(PostBaseForm):
    pass



class PostDeleteForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a post...',
                   }
        )
    )

class PostEditForm(PostBaseForm):
    pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')

        labels = {
            'author': '',
            'content': '',
        }

        error_messages = {
            'author': {
                'required': 'Author name is required. Write it!',
            },
            'content': {
                'required': 'Content is required. Write it!',
            },
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your name',
        })

        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add message',
            'rows': 1
        })


CommentFormSet = formset_factory(CommentForm, extra=1)