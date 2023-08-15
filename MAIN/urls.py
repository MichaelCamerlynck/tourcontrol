from django.urls import path
from MAIN import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("home", views.IndexHomeView.as_view(), name='home'),
    path("contact", views.Contact.as_view(), name='contact'),
    path("send", views.send, name='send'),
]