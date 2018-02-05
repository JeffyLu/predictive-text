from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/predictive/', include('predictive.urls'))
]
