from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index),
    url(r'^$', views.register),
    url(r'^clear$', views.clear_words),
    url(r'^add_word$', views.add_word),
    url(r'^doRegister$', views.doRegistration),
    url(r'^login$', views.login),
    url(r'^test$', views.index)


]