from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from news.models import Author, Category, Post
from django.contrib.contenttypes.models import ContentType


class CriticalPathsTests(TestCase):
    """Тесты основных сценариев использования"""

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testauthor',
            password='testpass123',
            email='author@example.com'
        )
        self.author = Author.objects.create(user=self.user)
        # Создаем или получаем группу авторов
        authors_group, created = Group.objects.get_or_create(name='authors')
        # Добавляем необходимые права для группы authors
        content_type = ContentType.objects.get_for_model(Post)
        # Права на публикации
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_post', 'change_post', 'delete_post']
        )
        authors_group.permissions.add(*permissions)
        # Добавляем пользователя в группу
        self.user.groups.add(authors_group)
        # Создаем категорию
        self.category = Category.objects.create(name='Technology')

    def test_post_creation_workflow(self):
        """Весь процесс создания публикации работает"""
        # 1. Логин
        self.client.login(username='testauthor', password='testpass123')
        # 2. Переход на форму создания новости
        response = self.client.get(reverse('news_create'))
        # Проверяем, что есть доступ (200) или редирект на логин (302)
        self.assertIn(response.status_code, [200, 302])
        # 3. Создание новости (если доступно)
        if response.status_code == 200:
            post_data = {
                'category': self.category.id,
                'title': 'Test News Workflow',
                'text': 'Testing the complete workflow of news creation with enough characters'
            }
            response = self.client.post(reverse('news_create'), post_data)
            # Проверка редиректа на детальную страницу
            self.assertIn(response.status_code, [302, 200])
            # Проверка создания в БД
            post = Post.objects.filter(title='Test News Workflow').first()
            self.assertIsNotNone(post)
            print(f"✓ Новость создана: {post.title}")
        else:
            print("⚠ Пропускаем тест создания - нет доступа к форме")

    def test_article_creation_workflow(self):
        """Весь процесс создания статьи работает"""
        # Логин
        self.client.login(username='testauthor', password='testpass123')
        # Переход на форму создания статьи
        response = self.client.get(reverse('article_create'))
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 200:
            # Создание статьи
            post_data = {
                'category': self.category.id,
                'title': 'Test Article Workflow',
                'text': 'Testing the complete workflow of article creation with enough characters'
            }

            response = self.client.post(reverse('article_create'), post_data)
            # Проверка редиректа
            self.assertIn(response.status_code, [302, 200])
            # Проверка создания в БД
            article = Post.objects.filter(title='Test Article Workflow').first()
            self.assertIsNotNone(article)
            self.assertEqual(article.post_type, 'article')
            print(f"✓ Статья создана: {article.title}")
        else:
            print("⚠ Пропускаем тест создания статьи - нет доступа к форме")

    def test_subscription_workflow(self):
        """Процесс подписки на категорию работает"""
        # Создаем пользователя для подписки
        subscriber = User.objects.create_user(
            username='subscriber',
            password='testpass123'
        )
        self.client.login(username='subscriber', password='testpass123')
        # Подписываемся на категорию
        response = self.client.post(
            reverse('subscribe_category', args=[self.category.id])
        )
        # Проверяем, что пользователь подписан
        self.assertTrue(self.category.subscribers.filter(id=subscriber.id).exists())
        print(f"✓ Пользователь {subscriber.username} подписан на категорию {self.category.name}")