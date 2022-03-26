from django.urls import path
from api_v1.views import ArticlesListView, ArticleDetailView, get_csrf_token_view

app_name = 'api_v1'


urlpatterns = [
    path('get-csrf-token/', get_csrf_token_view),
    path('articles/', ArticlesListView.as_view()),
    path('article/<int:pk>', ArticleDetailView.as_view())
]
