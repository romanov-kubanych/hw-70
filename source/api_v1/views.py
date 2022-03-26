from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.serializers import ArticleSerializer, ArticleExtendedSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_csrf_token_view(request):
    if request.method == "GET":
        return HttpResponse()
    return HttpResponseNotAllowed(["GET"])


class ArticlesListView(APIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)

        serializer = ArticleSerializer(data=request.data, instance=article)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer_extended = ArticleExtendedSerializer(article)

        return Response(serializer_extended.data)

    def delete(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        response_data = {
            "id": article.id
        }
        article.delete()

        return Response(response_data)
