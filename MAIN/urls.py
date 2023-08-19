from django.urls import path
from MAIN import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("home", views.IndexHomeView.as_view(), name='home'),
    path("contact", views.Contact.as_view(), name='contact'),
    path("send", views.send, name='send'),
    path("blog", views.BlogListView.as_view(), name='blog'),
    path("blog/<int:pk>", views.BlogDetailView.as_view(), name='blog'),
    path('switch-language/<str:language_code>/', views.switch_language, name='switch_language'),

    path("home_admin", views.HomeSecret.as_view(), name='home_admin'),
    path("manage_members", views.ManageMembers.as_view(), name='manage_members'),
    path("manage_blogs_list", views.ManageBlogList.as_view(), name='manage_blogs_list'),
    path("manage_blog/<int:pk>", views.ManageBlog.as_view(), name='manage_blog'),
    path("delete_member", views.delete_member, name='delete_member'),
    path("manage_member", views.manage_member, name='manage_member'),
    path("new_blog", views.new_blog, name='new_blog'),
    path("save_blog", views.save_blog, name='save_blog'),
    path("delete_blog", views.delete_blog, name='delete_blog'),
]
