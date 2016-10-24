from rest_framework import serializers
from app.models import Article


class ArticleSerualizer(serializers.Serializer):
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

class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'header', 'content')