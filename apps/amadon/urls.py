from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^buy_item$', views.buy_item),
    url(r'^checkout$', views.checkout),
]