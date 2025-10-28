from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from.constants import BAD_WORDS


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
       model = Post
       fields = [
           'author',
           'category',
           'title',
           'text',
           'post_rating',
       ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text", "") or ""
        title = cleaned_data.get("title", "") or ""
        if title == text:
            raise ValidationError({
                "title": "The title cannot be identical to the text"
            })
        for word in BAD_WORDS:
            if word in title.lower():
                raise ValidationError({
                    "title": "The title should not contain bad words."
                })
            if word in text.lower():
                raise ValidationError({
                    "text": "The text should not contain bad words."
                })

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "The name must begin with a big letter"
            )
        return title