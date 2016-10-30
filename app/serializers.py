from rest_framework import serializers
from app.models import Article
from django.urls import reverse


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    header = serializers.CharField(allow_blank=True, max_length=500)
    content = serializers.CharField(allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return  Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.header = validated_data.get('header', instance.header)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

class ArticlesModelSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ('id', 'header', 'content', 'put_time', 'tag', 'click_rate', 'detail_url')

    def get_detail_url(self, obj):
        return reverse('detail', args=[obj.id, ''])


class ArticleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'header', 'content', 'put_time', 'tag', 'click_rate')
