from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news import views


router = routers.DefaultRouter()
router.register(r'author', views.AuthorViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'news', views.NewsViewSet, basename='news')
router.register(r'articles', views.ArticlesViewSet, basename='articles')
router.register(r'comment', views.CommentViewSet)
router.register(r'user', views.UserViewSet)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('groups/', include('accounts.urls')),
   path('', include('news.urls')),
   path('accounts/', include('allauth.urls')),
   path('i18n/', include('django.conf.urls.i18n')),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   path('api/', include(router.urls)),
]
