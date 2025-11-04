from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('groups/', include('accounts.urls')),
   path('', include('news.urls')),
   path('accounts/', include('allauth.urls')),
]
