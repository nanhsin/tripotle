from django.urls import path, include
from .views import SaveVocabViewSet, register_view, login_view, logout_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'savevocab', SaveVocabViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('savevocab/', SaveVocabViewSet.as_view({'post': 'save_vocab'}), name='savevocab'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]