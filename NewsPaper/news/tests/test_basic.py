from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from news.models import Author, Category, Post


class SmokeTests(TestCase):
    """Тест основных частей приложения"""

    def test_home_page_loads(self):
        """Главная страница загружается"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertTrue('News' in content or 'Новости' in content)

    def test_news_page_loads(self):
        """Страница новостей загружается"""
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_articles_page_loads(self):
        """Страница статей загружается"""
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        """Админ панель доступна"""
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302])


class ModelCreationTests(TestCase):
    """Тесты создания моделей"""

    def test_create_user_and_author(self):
        """Можно создать пользователя и автора"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        author = Author.objects.create(user=user)

        self.assertEqual(str(author), 'testuser')
        self.assertEqual(author.user.username, 'testuser')

    def test_create_category(self):
        """Можно создать категорию"""
        category = Category.objects.create(name='Technology')
        self.assertEqual(str(category), 'Technology')

    def test_create_post(self):
        """Можно создать публикацию"""
        user = User.objects.create_user(username='author', password='pass')
        author = Author.objects.create(user=user)
        category = Category.objects.create(name='Technology')

        post = Post.objects.create(
            author=author,
            post_type='news',
            title='Test News',
            text='Test content with more than 20 characters for validation'
        )
        post.category.add(category)

        self.assertEqual(post.title, 'Test News')
        self.assertEqual(post.author.user.username, 'author')
        self.assertEqual(post.post_type, 'news')
        self.assertEqual(post.category.first().name, 'Technology')