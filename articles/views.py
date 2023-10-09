# from config.settings import (
#     CLIENT_ID,
#     CLIENT_SECRET,
# )
# import urllib.request
import requests
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from articles.models import Product, Article
from articles.serializers import ProductInfoSerializer


# Create your views here.
class ArticleListView(APIView):
    def post(self, request, format=None):
        product_id = request.data.get("product_id")
        sim_products_endpoint = f"https://goods.musinsa.com/api/goods/v2/review/similar-list?goodsNo={product_id}"
        stats_endpoint = (
            f"https://www.musinsa.com/app/product/goodsview_stats/{product_id}"
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        sim_products_response = requests.get(sim_products_endpoint, headers=headers)
        stats_response = requests.get(stats_endpoint, headers=headers)
        if (
            sim_products_response.status_code == 200
            and stats_response.status_code == 200
        ):
            product = {"id": product_id}

            products_info = sim_products_response.json()
            for product_info in products_info["data"]:
                if int(product_info["goodsNo"]) == product_id:
                    product["name"] = product_info["goodsName"]
                    product["price"] = int(product_info["price"])
                    product["image"] = product_info["image"]
                    product["state"] = product_info["saleStatLabel"]

                    break
            stats = stats_response.json()
            product["quantity"] = stats["purchase"]["quantity"]
            product_obj = Product.objects.create(**product)
            serializer = ProductInfoSerializer(product_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "오류"})

        # brand = request.data.get("brand")
        # SKU = request.data.get("SKU")
        # if not (brand or SKU):
        #     return Response(
        #         {"detail": "브랜드와 품번을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST
        #     )
        # params = {
        #     "query": f"{brand} {SKU}",
        #     "exclude": "cbshop:used:rental",
        #     "display": 100,
        # }
        # query_string = urllib.parse.urlencode(params, encoding="utf-8")
        # print(query_string)
        # url = f"https://openapi.naver.com/v1/search/shop.json?{query_string}"
        # request = urllib.request.Request(url)
        # request.add_header("X-Naver-Client-Id", CLIENT_ID)
        # request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
        # response = urllib.request.urlopen(request)
        # rescode = response.getcode()
        # if rescode == 200:
        #     response_body = json.loads(response.read().decode("utf-8"))
        #     return Response(response_body)
        # else:
        #     print("Error Code:" + rescode)
        #     return Response()


class ArticleDetailView(APIView):
    pass


# class CommentView(APIView):
#     def get(self, request, article_id):
#         article = Article.objects.get(id=article_id)
#         comments = article.comment_set.all()
#         serializer =


class CommentDetailView(APIView):
    pass


class ArticleLikeView(APIView):
    pass


class CommentLikeView(APIView):
    pass
