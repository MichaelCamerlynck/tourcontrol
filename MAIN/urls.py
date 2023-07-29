from django.urls import path
from MAIN import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("op2", views.IndexView2.as_view(), name='op2'),
    path("op3", views.IndexView3.as_view(), name='op3'),
    path("contact", views.Contact.as_view(), name='contact'),
]