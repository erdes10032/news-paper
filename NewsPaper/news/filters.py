from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter, CharFilter
from django import forms
from django.utils.translation import gettext as _
from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Title')
    )

    category = ModelMultipleChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
        label=_('Category'),
        conjoined=True
    )

    creation_date_after = DateFilter(
        field_name='creation_date',
        lookup_expr='gt',
        label=_('Creation date after'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )


    class Meta:
        model = Post
        fields = []