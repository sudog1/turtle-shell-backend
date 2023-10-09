from rest_framework import serializers
from articles.models import Article,Comment, Product

class CommentListSerializers(serializers.ModelSerializer):

    author=serializers.SerializerMethodField()
    def get_author(self,obj):
        return User.objects.filte
    class Meta:
        model=Article
        fields=""
 


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
