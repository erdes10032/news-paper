from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from.constants import forbidden_words
from django.utils.translation import gettext as _


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20, label=_('Text'))

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
        ]
        labels = {
            'category': _('Category'),
            'title': _('Title'),
       }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text", "") or ""
        title = cleaned_data.get("title", "") or ""
        if title == text:
            raise ValidationError({
                "title": _("The title cannot be identical to the text")
            })
        for word in forbidden_words:
            if word in title.lower():
                raise ValidationError({
                    "title": _("The title should not contain bad words.")
                })
            if word in text.lower():
                raise ValidationError({
                    "text": _("The text should not contain bad words.")
                })

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                _("The title must begin with a big letter")
            )
        return title