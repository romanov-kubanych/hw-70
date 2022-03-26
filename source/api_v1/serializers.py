from rest_framework import serializers

from webapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']
        read_only_fields = ['author']


class ArticleExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = []
        read_only_fields = ['author', 'created_at', 'updated_at', 'tags']
