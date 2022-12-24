from django.urls import path
from . import views


app_name = 'src.blog'

urlpatterns = [
    path('blog/', views.post_list, name='post_list'),
    path('blog/<int:post_id>', views.post_detail, name='post_detail'),
]
