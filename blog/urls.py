from django.urls import path
# from .views import post_list_view
# from .views import post_detail_view
# from .views import post_create_view
# from .views import post_update_view
# from .views import post_delete_view
from .views import PostListView
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]

