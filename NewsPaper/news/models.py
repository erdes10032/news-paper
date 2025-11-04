from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site

POST_TYPES = [
    ('article', 'Article'),
    ('news', 'News'),
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(models.Sum('post_rating'))['post_rating__sum'] or 0
        posts_rating *= 3
        user_comments_rating = Comment.objects.filter(user = self.user).aggregate(models.Sum('comment_rating'))['comment_rating__sum'] or 0
        post_comments_rating = Comment.objects.filter(post__author = self).aggregate(models.Sum('comment_rating'))['comment_rating__sum'] or 0
        self.author_rating = posts_rating + user_comments_rating + post_comments_rating
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=7, choices=POST_TYPES, default='article')
    creation_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    post_rating = models.FloatField(default=0.0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            short_text = self.text[:124] + '...'
            return short_text
        else:
            return self.text

    def __str__(self):
        return f'{self.title} \n{self.preview()}'

    def get_absolute_url(self):
        if self.post_type == 'news':
            return reverse('news_detail', args=[str(self.id)])
        else:
            return reverse('article_detail', args=[str(self.id)])

    def get_absolute_url_with_domain(self):
        return f"http://{Site.objects.get_current().domain}:8000{self.get_absolute_url()}"

    def save(self, *args, **kwargs):
        if not self.pk and self.post_type == 'news':
            author = self.author
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_news_count = Post.objects.filter(
                author=author,
                post_type='news',
                creation_date__gte=today_start
            ).count()
            if today_news_count > 5:
                raise ValidationError(
                    'You cannot publish more than 3 news items per day.'
                )

        super().save(*args, **kwargs)

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class CategoryUser(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
