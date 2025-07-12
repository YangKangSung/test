import asyncio
from playwright.async_api import async_playwright
import json
import time
from urllib.parse import urljoin, urlparse

class MultiPageLinkScraper:
    def __init__(self, base_url, max_pages=10, max_links_per_page=20):
        self.base_url = base_url
        self.max_pages = max_pages
        self.max_links_per_page = max_links_per_page
        self.scraped_data = []
        self.visited_urls = set()
        
    async def scrape_all_pages(self):
        """모든 페이지의 링크를 스크래핑하는 메인 함수"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            try:
                page = await context.new_page()
                current_page = 1
                
                while current_page <= self.max_pages:
                    print(f"페이지 {current_page} 스크래핑 시작...")
                    
                    # 현재 페이지로 이동
                    page_url = self._get_page_url(current_page)
                    await page.goto(page_url, wait_until='networkidle')
                    
                    # 페이지의 링크들 수집
                    links = await self._collect_links_from_page(page)
                    
                    if not links:
                        print(f"페이지 {current_page}에서 링크를 찾을 수 없습니다.")
                        break
                    
                    print(f"페이지 {current_page}에서 {len(links)}개의 링크 발견")
                    
                    # 각 링크의 내용 스크래핑
                    for i, link in enumerate(links[:self.max_links_per_page]):
                        if link in self.visited_urls:
                            continue
                            
                        print(f"  링크 {i+1}/{len(links)} 스크래핑 중...")
                        content = await self._scrape_link_content(context, link)
                        
                        if content:
                            self.scraped_data.append({
                                'page_number': current_page,
                                'link_index': i + 1,
                                'url': link,
                                'content': content
                            })
                            self.visited_urls.add(link)
                        
                        # 요청 간 지연
                        await asyncio.sleep(1)
                    
                    # 다음 페이지 확인
                    if not await self._has_next_page(page):
                        print("다음 페이지가 없습니다.")
                        break
                    
                    current_page += 1
                    await asyncio.sleep(2)  # 페이지 간 지연
                    
            finally:
                await browser.close()
        
        return self.scraped_data
    
    def _get_page_url(self, page_number):
        """페이지 번호에 따른 URL 생성 (사이트에 맞게 수정 필요)"""
        if page_number == 1:
            return self.base_url
        # 일반적인 페이지네이션 패턴들
        # return f"{self.base_url}?page={page_number}"
        # return f"{self.base_url}/page/{page_number}"
        return f"{self.base_url}?p={page_number}"
    
    async def _collect_links_from_page(self, page):
        """현재 페이지에서 링크들을 수집"""
        try:
            # 일반적인 링크 선택자들 (사이트에 맞게 수정 필요)
            link_selectors = [
                'a[href*="/article/"]',  # 기사 링크
                'a[href*="/post/"]',     # 포스트 링크
                '.post-title a',         # 포스트 제목 링크
                '.article-title a',      # 기사 제목 링크
                'h2 a',                  # 제목 링크
                'h3 a',                  # 소제목 링크
            ]
            
            all_links = []
            
            for selector in link_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        href = await element.get_attribute('href')
                        if href:
                            full_url = urljoin(self.base_url, href)
                            if self._is_valid_url(full_url):
                                all_links.append(full_url)
                except:
                    continue
            
            # 중복 제거 및 개수 제한
            unique_links = list(dict.fromkeys(all_links))
            return unique_links[:self.max_links_per_page]
            
        except Exception as e:
            print(f"링크 수집 중 오류: {e}")
            return []
    
    async def _scrape_link_content(self, context, url):
        """개별 링크의 내용을 스크래핑"""
        try:
            page = await context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 페이지 내용 추출 (사이트에 맞게 수정 필요)
            content = await self._extract_content_from_page(page)
            
            await page.close()
            return content
            
        except Exception as e:
            print(f"링크 {url} 스크래핑 중 오류: {e}")
            return None
    
    async def _extract_content_from_page(self, page):
        """페이지에서 실제 내용을 추출"""
        try:
            # 제목 추출
            title = ""
            title_selectors = ['h1', '.post-title', '.article-title', 'title']
            for selector in title_selectors:
                try:
                    title_element = await page.query_selector(selector)
                    if title_element:
                        title = await title_element.inner_text()
                        break
                except:
                    continue
            
            # 본문 내용 추출
            content = ""
            content_selectors = [
                '.post-content',
                '.article-content', 
                '.content',
                'article',
                '.entry-content',
                'main'
            ]
            
            for selector in content_selectors:
                try:
                    content_element = await page.query_selector(selector)
                    if content_element:
                        content = await content_element.inner_text()
                        break
                except:
                    continue
            
            # 메타 정보 추출
            meta_info = await self._extract_meta_info(page)
            
            return {
                'title': title.strip(),
                'content': content.strip()[:2000],  # 내용 길이 제한
                'meta': meta_info,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"내용 추출 중 오류: {e}")
            return None
    
    async def _extract_meta_info(self, page):
        """메타 정보 추출"""
        meta_info = {}
        
        try:
            # 메타 태그들 추출
            meta_tags = await page.query_selector_all('meta')
            for meta in meta_tags:
                name = await meta.get_attribute('name')
                property_attr = await meta.get_attribute('property')
                content = await meta.get_attribute('content')
                
                if name and content:
                    meta_info[name] = content
                elif property_attr and content:
                    meta_info[property_attr] = content
                    
        except:
            pass
            
        return meta_info
    
    async def _has_next_page(self, page):
        """다음 페이지가 있는지 확인"""
        try:
            # 다음 페이지 버튼 찾기
            next_selectors = [
                'a[rel="next"]',
                '.next-page',
                '.pagination-next',
                'a:has-text("다음")',
                'a:has-text("Next")',
                'a:has-text(">")'
            ]
            
            for selector in next_selectors:
                try:
                    next_button = await page.query_selector(selector)
                    if next_button:
                        return True
                except:
                    continue
                    
            return False
            
        except:
            return False
    
    def _is_valid_url(self, url):
        """유효한 URL인지 확인"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except:
            return False
    
    def save_to_json(self, filename='scraped_data.json'):
        """결과를 JSON 파일로 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=2)
        print(f"데이터가 {filename}에 저장되었습니다.")

# 사용 예제
async def main():
    # 스크래핑할 사이트의 기본 URL 설정
    base_url = "https://example.com/news"  # 실제 URL로 변경
    
    # 스크래퍼 인스턴스 생성
    scraper = MultiPageLinkScraper(
        base_url=base_url,
        max_pages=5,           # 최대 5페이지까지
        max_links_per_page=20  # 페이지당 최대 20개 링크
    )
    
    # 스크래핑 실행
    print("스크래핑 시작...")
    results = await scraper.scrape_all_pages()
    
    # 결과 출력
    print(f"\n스크래핑 완료! 총 {len(results)}개의 링크 내용을 수집했습니다.")
    
    # JSON 파일로 저장
    scraper.save_to_json('scraped_results.json')
    
    # 결과 미리보기
    if results:
        print("\n=== 수집된 데이터 미리보기 ===")
        for i, item in enumerate(results[:3]):  # 처음 3개만 출력
            print(f"\n[{i+1}] 페이지 {item['page_number']}, 링크 {item['link_index']}")
            print(f"URL: {item['url']}")
            print(f"제목: {item['content']['title'][:100]}...")
            print(f"내용: {item['content']['content'][:200]}...")

# 실행
if __name__ == "__main__":
    asyncio.run(main())

# 설치 필요한 패키지:
# pip install playwright
# playwright install