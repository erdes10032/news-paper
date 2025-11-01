from .views import upgrade_me
from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('upgrade/', upgrade_me, name = 'upgrade')
]