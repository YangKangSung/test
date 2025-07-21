import json
import re
import time
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging
from datetime import datetime
import pandas as pd
from playwright.sync_api import sync_playwright

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PostData:
    """게시물 데이터 구조"""
    title: str
    content: str
    author: str
    post_date: str
    view_count: Optional[int]
    like_count: Optional[int]
    comment_count: Optional[int]
    post_url: str
    category: Optional[str]
    tags: List[str]

class MosaicScraper:
    """삼성 모자이크 커뮤니티 스크래퍼 (Playwright 버전)"""

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            locale='ko-KR'
        )
        self.page = self.context.new_page()
        self.base_url = "https://mosaic.sec.samsung.net"

    def __del__(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def fetch_page(self, url: str, retries: int = 3) -> Optional[bool]:
        """페이지 로드 with 재시도"""
        for attempt in range(retries):
            try:
                self.page.goto(url, timeout=10000)
                self.page.wait_for_selector('.post-list', timeout=5000)
                return True
            except Exception as e:
                logger.warning(f"페이지 로드 실패 (시도 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # 지수 백오프
                else:
                    logger.error(f"페이지 로드 최종 실패: {url}")
                    return False

    def clean_text(self, text: str) -> str:
        """텍스트 정제"""
        if not text:
            return ""
        # 불필요한 공백, 특수문자 제거 및 정규화
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s가-힣.,!?%()-]', '', text)
        return text

    def extract_post_info(self, post_elem) -> Optional[PostData]:
        """개별 게시물 정보 추출"""
        try:
            # 게시물 제목
            title_elem = post_elem.query_selector('.title a')
            title = self.clean_text(title_elem.inner_text()) if title_elem else "제목 없음"

            # 게시물 URL
            post_url = urljoin(self.base_url, title_elem.get_attribute('href')) if title_elem else ""

            # 작성자
            author_elem = post_elem.query_selector('.author')
            author = self.clean_text(author_elem.inner_text()) if author_elem else "작성자 없음"

            # 작성일
            date_elem = post_elem.query_selector('.date')
            post_date = self.clean_text(date_elem.inner_text()) if date_elem else "날짜 없음"

            # 조회수
            view_elem = post_elem.query_selector('.view-count')
            view_count = int(self.clean_text(view_elem.inner_text())) if view_elem else None

            # 좋아요 수
            like_elem = post_elem.query_selector('.like-count')
            like_count = int(self.clean_text(like_elem.inner_text())) if like_elem else None

            # 댓글 수
            comment_elem = post_elem.query_selector('.comment-count')
            comment_count = int(self.clean_text(comment_elem.inner_text())) if comment_elem else None

            # 카테고리
            category_elem = post_elem.query_selector('.category')
            category = self.clean_text(category_elem.inner_text()) if category_elem else None

            # 태그
            tag_elems = post_elem.query_selector_all('.tags a')
            tags = [self.clean_text(tag.inner_text()) for tag in tag_elems] if tag_elems else []

            return PostData(
                title=title,
                content="",  # 상세 페이지에서 추출
                author=author,
                post_date=post_date,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                post_url=post_url,
                category=category,
                tags=tags
            )

        except Exception as e:
            logger.error(f"게시물 정보 추출 중 오류: {e}")
            return None

    def enhance_post_data(self, post: PostData) -> PostData:
        """게시물 상세 페이지에서 내용 추출"""
        if not post.post_url:
            return post

        if not self.fetch_page(post.post_url):
            return post

        try:
            # 게시물 내용 추출
            content_elem = self.page.query_selector('.post-content')
            if content_elem:
                post.content = self.clean_text(content_elem.inner_text())

        except Exception as e:
            logger.error(f"게시물 상세 정보 추출 중 오류: {e}")

        time.sleep(0.5)  # 요청 간격 조절
        return post

    def scrape_post_list(self, url: str) -> List[PostData]:
        """게시물 목록 페이지 스크래핑"""
        if not self.fetch_page(url):
            return []

        posts = []
        post_elements = self.page.query_selector_all('.post-list .post-item')

        if not post_elements:
            logger.warning("게시물 요소를 찾을 수 없습니다.")
            return []

        for elem in post_elements:
            post_data = self.extract_post_info(elem)
            if post_data:
                posts.append(post_data)

        logger.info(f"총 {len(posts)}개 게시물 정보 추출 완료")
        return posts

    def get_all_pages(self, start_url: str, max_pages: int = 10) -> List[PostData]:
        """모든 페이지의 게시물 수집"""
        all_posts = []
        current_url = start_url
        page_count = 0

        while current_url and page_count < max_pages:
            logger.info(f"페이지 {page_count + 1} 처리 중...")
            posts = self.scrape_post_list(current_url)
            all_posts.extend(posts)

            # 다음 페이지 URL 찾기
            next_link = self.page.query_selector('.pagination .next a')
            current_url = urljoin(self.base_url, next_link.get_attribute('href')) if next_link else None
            page_count += 1

            time.sleep(1)  # 페이지 간 요청 간격

        return all_posts

class RAGDataProcessor:
    """RAG 시스템을 위한 데이터 전처리"""

    def __init__(self):
        self.processed_data = []

    def create_rag_document(self, post: PostData) -> Dict:
        """RAG용 문서 생성"""
        # 게시물 정보를 자연어 형태로 구성
        doc_content = []

        # 기본 정보
        doc_content.append(f"제목: {post.title}")
        doc_content.append(f"작성자: {post.author}")
        doc_content.append(f"작성일: {post.post_date}")

        if post.category:
            doc_content.append(f"카테고리: {post.category}")

        # 통계 정보
        stats = []
        if post.view_count is not None:
            stats.append(f"조회수: {post.view_count}")
        if post.like_count is not None:
            stats.append(f"좋아요: {post.like_count}")
        if post.comment_count is not None:
            stats.append(f"댓글: {post.comment_count}")

        if stats:
            doc_content.append(" | ".join(stats))

        # 태그 정보
        if post.tags:
            doc_content.append(f"태그: {', '.join(post.tags)}")

        # 게시물 내용
        if post.content:
            doc_content.append(f"내용: {post.content}")

        # 메타데이터
        metadata = {
            "post_url": post.post_url,
            "author": post.author,
            "post_date": post.post_date,
            "category": post.category,
            "tags": post.tags,
            "scraped_at": datetime.now().isoformat()
        }

        return {
            "id": self.generate_doc_id(post),
            "content": "\n".join(doc_content),
            "metadata": metadata,
            "title": post.title
        }

    def generate_doc_id(self, post: PostData) -> str:
        """문서 ID 생성"""
        import hashlib
        content = f"{post.title}_{post.post_url}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def process_posts(self, posts: List[PostData]) -> List[Dict]:
        """게시물 리스트를 RAG 문서로 변환"""
        rag_documents = []

        for post in posts:
            try:
                enhanced_post = self.enhance_post_data(post)
                doc = self.create_rag_document(enhanced_post)
                rag_documents.append(doc)
            except Exception as e:
                logger.error(f"문서 생성 중 오류: {e}")

        return rag_documents

    def save_to_files(self, documents: List[Dict], output_prefix: str = "mosaic_posts"):
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
                'post_url': doc['metadata'].get('post_url', ''),
                'author': doc['metadata'].get('author', ''),
                'post_date': doc['metadata'].get('post_date', ''),
                'category': doc['metadata'].get('category', '')
            }
            csv_data.append(row)

        df = pd.DataFrame(csv_data)
        csv_filename = f"{output_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        logger.info(f"CSV 파일 저장 완료: {csv_filename}")

def main():
    """메인 실행 함수"""
    # 스크래퍼 초기화
    scraper = MosaicScraper()
    rag_processor = RAGDataProcessor()

    # 스크래핑 대상 URL
    target_url = "https://mosaic.sec.samsung.net/kms/comty.do?comtyId=158843131&menuId=2043836422&page=list&type=LIST"

    logger.info("삼성 모자이크 커뮤니티 페이지 스크래핑 시작 (Playwright 버전)")

    # 게시물 데이터 수집 (처음 3페이지만 - 시간 절약)
    posts = scraper.get_all_pages(target_url, max_pages=3)

    if not posts:
        logger.error("게시물 데이터를 수집할 수 없습니다.")
        return

    logger.info(f"{len(posts)}개 게시물 기본 정보 수집 완료")

    # RAG 문서 생성
    logger.info("RAG 문서 생성 중...")
    rag_documents = rag_processor.process_posts(posts)

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