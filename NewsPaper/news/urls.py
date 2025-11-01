from django.urls import path
from .views import NewsList, ArticlesList, NewsDetail, ArticleDetail, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete, NewsOrArticleView


urlpatterns = [
   path('', NewsOrArticleView.as_view(), name='news_or_article'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('article/', ArticlesList.as_view(), name='article_list'),
   path('news/<int:pk>', NewsDetail.as_view(), name = 'news_detail'),
   path('article/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete')
]