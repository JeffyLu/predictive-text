from django.conf.urls import url, include
from rest_framework import routers
from predictive import views


router = routers.DefaultRouter()
router.register(r'vocabularies', views.VocabularyViewSet,
                base_name='invitations')
router.register(r'phrases', views.PhraseViewSet,
                base_name='phrases')

urlpatterns = [
    url(r'^', include(router.urls))
]
