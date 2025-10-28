from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter
from django import forms
from .models import Post, Category


class PostFilter(FilterSet):

    category = ModelMultipleChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
        label="Category",
        conjoined=True
    )

    creation_date_after = DateFilter(
        field_name='creation_date',
        lookup_expr='gt',
        label='Publication date after',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains']
        }