from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post, Category
from rest_framework import viewsets, permissions
from .serializers import *
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.core.cache import cache
import pytz
from django.utils.translation import gettext as _


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='news')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='article')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NewsList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='news')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['post_type'] = 'news'
        return context


class ArticlesList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='article')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['post_type'] = 'article'
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(post_type='news')

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


class ArticleDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(post_type='article')

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'article-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'article-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.post_type = 'news'
        form.instance.author = author
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.post_type = 'article'
        form.instance.author = author
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            author = Author.objects.get(user=request.user)
            if self.get_object().author != author and not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied(_("You can edit only your own posts"))
        return super().dispatch(request, *args, **kwargs)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            author = Author.objects.get(user=request.user)
            if self.get_object().author != author and not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied(_("You can edit only your own posts"))
        return super().dispatch(request, *args, **kwargs)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            author = Author.objects.get(user=request.user)
            if self.get_object().author != author and not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied(_("You can delete only your own posts"))
        return super().dispatch(request, *args, **kwargs)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            author = Author.objects.get(user=request.user)
            if self.get_object().author != author and not request.user.groups.filter(name='admin').exists():
                raise PermissionDenied(_("You can delete only your own posts"))
        return super().dispatch(request, *args, **kwargs)


class MainPage(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


@login_required()
def subscribe_to_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if not category.subscribers.filter(id = request.user.id).exists():
        category.subscribers.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))