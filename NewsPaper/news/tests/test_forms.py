from django.test import TestCase
from news.forms import PostForm
from news.models import Category, Author
from django.contrib.auth.models import User


class FormValidationTests(TestCase):
    """Тесты валидации форм"""

    def setUp(self):
        # Создаем тестовые данные
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.author = Author.objects.create(user=self.user)
        self.category = Category.objects.create(name='Technology')

    def test_post_form_validation(self):
        """Форма публикации правильно валидируется"""
        # Хорошие данные
        good_data = {
            'category': [self.category.id],  # Для ManyToMany поле нужен список
            'title': 'Valid Title',
            'text': 'This is valid text with more than 20 characters'
        }
        form = PostForm(data=good_data)
        self.assertTrue(form.is_valid())

        # Плохие данные - короткий текст (меньше 20 символов)
        bad_data_short = {
            'category': [self.category.id],
            'title': 'Short Text',
            'text': 'Short'  # Меньше 20 символов
        }
        form = PostForm(data=bad_data_short)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

        # Плохие данные - заголовок с маленькой буквы (но с длинным текстом!)
        bad_data_lowercase = {
            'category': [self.category.id],
            'title': 'invalid title',  # маленькая буква
            'text': 'Valid text with more than 20 characters for validation test'  # длинный текст
        }
        form = PostForm(data=bad_data_lowercase)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Плохие данные - одинаковые заголовок и текст
        same_text = 'Exactly the same text for both title and content with enough characters'
        bad_data_same = {
            'category': [self.category.id],
            'title': same_text,
            'text': same_text
        }
        form = PostForm(data=bad_data_same)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Плохие данные - запрещенное слово в заголовке
        bad_data_forbidden_title = {
            'category': [self.category.id],
            'title': 'Title with fuck inside',
            'text': 'Valid text with more than 20 characters for validation test'
        }
        form = PostForm(data=bad_data_forbidden_title)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Плохие данные - запрещенное слово в тексте
        bad_data_forbidden_text = {
            'category': [self.category.id],
            'title': 'Valid Title',
            'text': 'Text contains shit and more than 20 characters for validation'
        }
        form = PostForm(data=bad_data_forbidden_text)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)