from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .models import Brand, Product
from .serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
    BrandSerializer,
)
import requests
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime, timedelta
from config.settings import (
    BRAND_UPDATE_PERIOD,
    PRODUCT_UPDATE_PERIOD,
    API_ENDPOINT,
    USER_AGENT,
)


class ProductView(APIView):
    # 무신사 상품 페이지 스크래핑
    def scrape_mss(self, product_id):
        headers = {
            "User-Agent": USER_AGENT,
        }
        response = requests.get(f"{API_ENDPOINT}{product_id}", headers=headers)

        if response.status_code == 200:
            only_product_info = SoupStrainer("div", {"id": "page_product_detail"})
            soup = BeautifulSoup(
                response.text,
                "lxml",
                parse_only=only_product_info,
            ).findChild()
            page = soup.find("div", "page_detail_product", recursive=False)
            product_dict = {"id": product_id}
            brand_dict = {}
            brand_dict["image"] = (
                page.find("div", "detail_brand_banner", recursive=False)
                .find("p", "brandBanner")
                .find("img")
                .get("src")
            )
            product_summary = page.find(
                "div", "section_product_summary", recursive=False
            )
            product_dict["name"] = (
                product_summary.find("span", "product_title", recursive=False)
                .find("em")
                .text
            )
            wrap_product = product_summary.find("div", "wrap_product", recursive=False)
            product_dict["image"] = (
                wrap_product.find("div", "product_left", recursive=False)
                .find("div", id="detail_bigimg", recursive=False)
                .find("div", "product-img", recursive=False)
                .find("img")
                .get("src")
            )
            product_order_info = wrap_product.find(
                "div", id="product_order_info", recursive=False
            )
            brand_dict["name"], product_dict["SKU"] = map(
                lambda x: x.strip(),
                product_order_info.find("div", "product_info_section", recursive=False)
                .find("ul", "product_article")
                .find("li", recursive=False)
                .find("p", "product_article_contents", recursive=False)
                .find("strong")
                .text.split("/"),
            )
            product_dict["price"] = (
                product_order_info.find("div", "price_info_section", recursive=False)
                .find("ul", "product_article")
                .find("li", id="normal_price")
                .text
            )
            return {
                "brand_data": brand_dict,
                "product_data": product_dict,
            }
        else:
            return False

    def get(self, request, product_id=None, format=None):
        # 상품 상세(업데이트)
        if product_id:
            product = get_object_or_404(
                Product.objects.select_related("brand"), pk=product_id
            )
            # 상품 업데이트 시기가 되지 않음
            if datetime.now() - product.updated_at < timedelta(
                minutes=PRODUCT_UPDATE_PERIOD
            ):
                serializer = ProductDetailSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # 상품 업데이트
            # 무신사 페이지 스크래핑
            result = self.scrape_mss(product_id)
            if result:
                brand_data = result["brand_data"]
                product_data = result["product_data"]
                # 브랜드 업데이트 시기가 지났으면 업데이트
                if datetime.now() - product.brand.updated_at >= timedelta(
                    minutes=BRAND_UPDATE_PERIOD
                ):
                    brand_serializer = BrandSerializer(product.brand, data=brand_data)
                    if brand_serializer.is_valid():
                        brand_serializer.save()
                product_data["brand"] = product.brand.pk
                serializer = ProductDetailSerializer(product, data=product_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "상품페이지 요청 실패."}, status=status.HTTP_400_BAD_REQUEST
                )
        # 전체 상품 리스트
        else:
            products = Product.objects.all()
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 작성 시 상품 등록
    def post(self, request, format=None):
        product_id = request.data.get("product_id")
        # 상품 등록(상품이 존재하므로 업데이트)
        if Product.objects.filter(pk=product_id).exists():
            product = Product.objects.select_related("brand").get(pk=product_id)
            # 상품 업데이트 시기가 되지 않음
            if datetime.now() - product.updated_at < timedelta(
                minutes=PRODUCT_UPDATE_PERIOD
            ):
                serializer = ProductListSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # 상품 업데이트
            result = self.scrape_mss(product_id)
            if result:
                brand_data = result["brand_data"]
                product_data = result["product_data"]
                # 브랜드 업데이트
                if datetime.now() - product.brand.updated_at >= timedelta(
                    minutes=BRAND_UPDATE_PERIOD
                ):
                    brand_serializer = BrandSerializer(product.brand, data=brand_data)
                    if brand_serializer.is_valid():
                        brand_serializer.save()
                product_data["brand"] = product.brand.pk
                serializer = ProductDetailSerializer(product, data=product_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "상품페이지 요청 실패."}, status=status.HTTP_400_BAD_REQUEST
                )
        # 상품 등록(상품이 데이터베이스에 없는 경우)
        else:
            result = self.scrape_mss(product_id)
            if result:
                brand_data = result["brand_data"]
                # 브랜드는 이미 존재할 수도 있고, 생성해야 할 수도 있습니다.
                if Brand.objects.filter(name=brand_data["name"]).exists():
                    brand = Brand.objects.get(name=brand_data["name"])
                    if datetime.now() - brand.updated_at >= timedelta(
                        minutes=BRAND_UPDATE_PERIOD
                    ):
                        brand_serializer = BrandSerializer(brand, data=brand_data)
                        if brand_serializer.is_valid():
                            brand_serializer.save()
                # 반드시 브랜드 생성을 먼저 해야 상품을 생성할 수 있습니다.
                else:
                    brand_serializer = BrandSerializer(data=brand_data)
                    if brand_serializer.is_valid():
                        brand = brand_serializer.save()

                product_data = result["product_data"]
                product_data["brand"] = brand.pk
                serializer = ProductDetailSerializer(data=product_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "상품페이지 요청 실패."}, status=status.HTTP_400_BAD_REQUEST
                )
                        