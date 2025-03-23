from django.urls import path, include
from .views import SaveVocabViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'savevocab', SaveVocabViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('savevocab/', SaveVocabViewSet.as_view({'post': 'save_vocab'}), name='savevocab'),
]