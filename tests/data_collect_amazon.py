import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging
from datetime import datetime
import pandas as pd

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ProductData:
    """상품 데이터 구조"""
    title: str
    price: Optional[str]
    original_price: Optional[str]
    discount_rate: Optional[str]
    rating: Optional[str]
    review_count: Optional[str]
    image_url: Optional[str]
    product_url: str
    description: Optional[str]
    seller: Optional[str]
    category: Optional[str]
    brand: Optional[str]
    shipping_info: Optional[str]
    features: List[str]

class ElevenStAmazonScraper:
    """11번가 아마존 페이지 스크래퍼"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.base_url = "https://www.11st.co.kr"

    def fetch_page(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """페이지 가져오기 with 재시도"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                logger.warning(f"페이지 요청 실패 (시도 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # 지수 백오프
                else:
                    logger.error(f"페이지 가져오기 최종 실패: {url}")
                    return None

    def clean_text(self, text: str) -> str:
        """텍스트 정제"""
        if not text:
            return ""
        # 불필요한 공백, 특수문자 제거 및 정규화
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s가-힣.,!?%()-]', '', text)
        return text

    def extract_price(self, element) -> Dict[str, Optional[str]]:
        """가격 정보 추출"""
        price_info = {"price": None, "original_price": None, "discount_rate": None}

        if not element:
            return price_info

        # 현재 가격
        price_elem = element.find(['span', 'strong'], class_=re.compile(r'price|cost|amount'))
        if price_elem:
            price_info["price"] = self.clean_text(price_elem.get_text())

        # 원래 가격 (할인 전)
        original_price_elem = element.find(['span', 'del'], class_=re.compile(r'origin|before|original'))
        if original_price_elem:
            price_info["original_price"] = self.clean_text(original_price_elem.get_text())

        # 할인율
        discount_elem = element.find(['span', 'em'], class_=re.compile(r'discount|sale|percent'))
        if discount_elem:
            price_info["discount_rate"] = self.clean_text(discount_elem.get_text())

        return price_info

    def extract_rating_info(self, element) -> Dict[str, Optional[str]]:
        """평점 정보 추출"""
        rating_info = {"rating": None, "review_count": None}

        if not element:
            return rating_info

        # 평점
        rating_elem = element.find(['span', 'div'], class_=re.compile(r'rating|star|score'))
        if rating_elem:
            rating_info["rating"] = self.clean_text(rating_elem.get_text())

        # 리뷰 수
        review_elem = element.find(['span', 'a'], class_=re.compile(r'review|comment|count'))
        if review_elem:
            rating_info["review_count"] = self.clean_text(review_elem.get_text())

        return rating_info

    def extract_product_features(self, soup: BeautifulSoup) -> List[str]:
        """상품 특징/스펙 추출"""
        features = []

        # 여러 가능한 특징 섹션 찾기
        feature_selectors = [
            '.spec-list li',
            '.feature-list li',
            '.product-info li',
            '[class*="spec"] li',
            '[class*="feature"] li'
        ]

        for selector in feature_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = self.clean_text(elem.get_text())
                if text and len(text) > 3:  # 의미있는 텍스트만
                    features.append(text)

        return list(set(features))  # 중복 제거

    def extract_product_info(self, product_elem, base_url: str) -> Optional[ProductData]:
        """개별 상품 정보 추출"""
        try:
            # 상품 제목
            title_elem = product_elem.find(['h3', 'h4', 'a'], class_=re.compile(r'title|name|product'))
            if not title_elem:
                title_elem = product_elem.find('a')
            title = self.clean_text(title_elem.get_text()) if title_elem else "제목 없음"

            # 상품 URL
            link_elem = product_elem.find('a', href=True)
            product_url = urljoin(base_url, link_elem['href']) if link_elem else ""

            # 가격 정보
            price_info = self.extract_price(product_elem)

            # 평점 정보
            rating_info = self.extract_rating_info(product_elem)

            # 이미지 URL
            img_elem = product_elem.find('img')
            image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
            if image_url:
                image_url = urljoin(base_url, image_url)

            # 판매자 정보
            seller_elem = product_elem.find(['span', 'div'], class_=re.compile(r'seller|shop|store'))
            seller = self.clean_text(seller_elem.get_text()) if seller_elem else None

            # 브랜드 정보
            brand_elem = product_elem.find(['span', 'div'], class_=re.compile(r'brand|maker'))
            brand = self.clean_text(brand_elem.get_text()) if brand_elem else None

            # 배송 정보
            shipping_elem = product_elem.find(['span', 'div'], class_=re.compile(r'shipping|delivery'))
            shipping_info = self.clean_text(shipping_elem.get_text()) if shipping_elem else None

            # 상품 설명 (간단한)
            desc_elem = product_elem.find(['p', 'div'], class_=re.compile(r'desc|summary|info'))
            description = self.clean_text(desc_elem.get_text()) if desc_elem else None

            return ProductData(
                title=title,
                price=price_info["price"],
                original_price=price_info["original_price"],
                discount_rate=price_info["discount_rate"],
                rating=rating_info["rating"],
                review_count=rating_info["review_count"],
                image_url=image_url,
                product_url=product_url,
                description=description,
                seller=seller,
                category=None,  # 페이지별로 설정
                brand=brand,
                shipping_info=shipping_info,
                features=[]  # 상세 페이지에서 추출
            )

        except Exception as e:
            logger.error(f"상품 정보 추출 중 오류: {e}")
            return None

    def scrape_product_list(self, url: str) -> List[ProductData]:
        """상품 목록 페이지 스크래핑"""
        soup = self.fetch_page(url)
        if not soup:
            return []

        products = []

        # 다양한 상품 리스트 셀렉터 시도
        product_selectors = [
            '.product-item',
            '.item',
            '.goods-item',
            '[class*="product"]',
            '.list-item',
            'li[class*="item"]'
        ]

        for selector in product_selectors:
            product_elements = soup.select(selector)
            if product_elements:
                logger.info(f"'{selector}' 셀렉터로 {len(product_elements)}개 상품 발견")
                break
        else:
            logger.warning("상품 요소를 찾을 수 없습니다.")
            return []

        for elem in product_elements:
            product_data = self.extract_product_info(elem, self.base_url)
            if product_data:
                products.append(product_data)

        logger.info(f"총 {len(products)}개 상품 정보 추출 완료")
        return products

    def enhance_product_data(self, product: ProductData) -> ProductData:
        """상품 상세 페이지에서 추가 정보 수집"""
        if not product.product_url:
            return product

        soup = self.fetch_page(product.product_url)
        if not soup:
            return product

        try:
            # 상세 설명 추출
            if not product.description:
                desc_selectors = ['.product-description', '.detail-info', '.product-detail']
                for selector in desc_selectors:
                    desc_elem = soup.select_one(selector)
                    if desc_elem:
                        product.description = self.clean_text(desc_elem.get_text()[:500])  # 처음 500자
                        break

            # 특징/스펙 추출
            product.features = self.extract_product_features(soup)

            # 카테고리 정보
            breadcrumb = soup.select('.breadcrumb a, .category a')
            if breadcrumb:
                categories = [self.clean_text(elem.get_text()) for elem in breadcrumb]
                product.category = " > ".join(categories)

        except Exception as e:
            logger.error(f"상품 상세 정보 추출 중 오류: {e}")

        time.sleep(0.5)  # 요청 간격 조절
        return product

class RAGDataProcessor:
    """RAG 시스템을 위한 데이터 전처리"""

    def __init__(self):
        self.processed_data = []

    def create_rag_document(self, product: ProductData) -> Dict:
        """RAG용 문서 생성"""
        # 상품 정보를 자연어 형태로 구성
        doc_content = []

        # 기본 정보
        doc_content.append(f"상품명: {product.title}")

        if product.brand:
            doc_content.append(f"브랜드: {product.brand}")

        if product.category:
            doc_content.append(f"카테고리: {product.category}")

        # 가격 정보
        price_info = []
        if product.price:
            price_info.append(f"가격: {product.price}")
        if product.original_price:
            price_info.append(f"정가: {product.original_price}")
        if product.discount_rate:
            price_info.append(f"할인율: {product.discount_rate}")

        if price_info:
            doc_content.append(" | ".join(price_info))

        # 평점 정보
        if product.rating or product.review_count:
            rating_text = []
            if product.rating:
                rating_text.append(f"평점: {product.rating}")
            if product.review_count:
                rating_text.append(f"리뷰수: {product.review_count}")
            doc_content.append(" | ".join(rating_text))

        # 판매자 및 배송
        if product.seller:
            doc_content.append(f"판매자: {product.seller}")
        if product.shipping_info:
            doc_content.append(f"배송: {product.shipping_info}")

        # 상품 설명
        if product.description:
            doc_content.append(f"설명: {product.description}")

        # 특징/스펙
        if product.features:
            features_text = " | ".join(product.features[:5])  # 상위 5개만
            doc_content.append(f"특징: {features_text}")

        # 메타데이터
        metadata = {
            "product_url": product.product_url,
            "image_url": product.image_url,
            "price_numeric": self.extract_numeric_price(product.price),
            "has_discount": bool(product.discount_rate),
            "category": product.category,
            "brand": product.brand,
            "scraped_at": datetime.now().isoformat()
        }

        return {
            "id": self.generate_doc_id(product),
            "content": "\n".join(doc_content),
            "metadata": metadata,
            "title": product.title
        }

    def extract_numeric_price(self, price_str: str) -> Optional[float]:
        """가격 문자열에서 숫자 추출"""
        if not price_str:
            return None

        # 숫자와 콤마만 추출
        numbers = re.findall(r'[\d,]+', price_str)
        if numbers:
            try:
                return float(numbers[0].replace(',', ''))
            except ValueError:
                return None
        return None

    def generate_doc_id(self, product: ProductData) -> str:
        """문서 ID 생성"""
        import hashlib
        content = f"{product.title}_{product.product_url}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def process_products(self, products: List[ProductData]) -> List[Dict]:
        """상품 리스트를 RAG 문서로 변환"""
        rag_documents = []

        for product in products:
            try:
                doc = self.create_rag_document(product)
                rag_documents.append(doc)
            except Exception as e:
                logger.error(f"문서 생성 중 오류: {e}")

        return rag_documents

    def save_to_files(self, documents: List[Dict], output_prefix: str = "11st_amazon_products"):
        """다양한 형식으로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON 저장 (RAG 시스템용)
        json_filename = f"{output_prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
        logger.info(f"JSON 파일 저장 완료: {json_filename}")

        # CSV 저장 (분석용)
        csv_data = []
        for doc in documents:
            row = {
                'id': doc['id'],
                'title': doc['title'],
                'content': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content'],
                'product_url': doc['metadata'].get('product_url', ''),
                'price': doc['metadata'].get('price_numeric', ''),
                'category': doc['metadata'].get('category', ''),
                'brand': doc['metadata'].get('brand', '')
            }
            csv_data.append(row)

        df = pd.DataFrame(csv_data)
        csv_filename = f"{output_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        logger.info(f"CSV 파일 저장 완료: {csv_filename}")

def main():
    """메인 실행 함수"""
    # 스크래퍼 초기화
    scraper = ElevenStAmazonScraper()
    rag_processor = RAGDataProcessor()

    # 스크래핑 대상 URL
    target_url = "https://www.11st.co.kr/amazon/"

    logger.info("11번가 아마존 페이지 스크래핑 시작")

    # 상품 데이터 수집
    products = scraper.scrape_product_list(target_url)

    if not products:
        logger.error("상품 데이터를 수집할 수 없습니다.")
        return

    logger.info(f"{len(products)}개 상품 기본 정보 수집 완료")

    # 상세 정보 보강 (처음 10개만 - 시간 절약)
    logger.info("상품 상세 정보 수집 중...")
    enhanced_products = []
    for i, product in enumerate(products[:10]):  # 처음 10개만
        logger.info(f"상세 정보 수집 중... ({i+1}/10)")
        enhanced_product = scraper.enhance_product_data(product)
        enhanced_products.append(enhanced_product)

    # 나머지는 기본 정보만 사용
    enhanced_products.extend(products[10:])

    # RAG 문서 생성
    logger.info("RAG 문서 생성 중...")
    rag_documents = rag_processor.process_products(enhanced_products)

    # 파일 저장
    rag_processor.save_to_files(rag_documents)

    logger.info(f"처리 완료! 총 {len(rag_documents)}개 문서 생성")

    # 샘플 출력
    if rag_documents:
        print("\n=== 샘플 RAG 문서 ===")
        sample_doc = rag_documents[0]
        print(f"ID: {sample_doc['id']}")
        print(f"제목: {sample_doc['title']}")
        print(f"내용: {sample_doc['content'][:300]}...")
        print(f"메타데이터: {json.dumps(sample_doc['metadata'], ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    main()