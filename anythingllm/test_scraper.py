import asyncio
from playwright.async_api import async_playwright
import json
import time
from urllib.parse import urljoin

class TestScraper:
    def __init__(self):
        self.scraped_data = []
        self.visited_urls = set()
        
    async def test_quotes_site(self):
        """Quotes to Scrape 사이트 테스트"""
        print("=== Quotes to Scrape 테스트 시작 ===")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # 브라우저 창을 보려면 False
            page = await browser.new_page()
            
            try:
                base_url = "http://quotes.toscrape.com"
                current_page = 1
                max_pages = 3
                
                while current_page <= max_pages:
                    if current_page == 1:
                        url = base_url
                    else:
                        url = f"{base_url}/page/{current_page}/"
                    
                    print(f"\n페이지 {current_page} 스크래핑: {url}")
                    await page.goto(url)
                    
                    # 명언 수집
                    quotes = await page.query_selector_all('.quote')
                    print(f"발견된 명언 수: {len(quotes)}")
                    
                    for i, quote in enumerate(quotes):
                        try:
                            text = await quote.query_selector('.text')
                            author = await quote.query_selector('.author')
                            tags = await quote.query_selector_all('.tag')
                            
                            quote_text = await text.inner_text() if text else ""
                            author_name = await author.inner_text() if author else ""
                            tag_list = []
                            
                            for tag in tags:
                                tag_text = await tag.inner_text()
                                tag_list.append(tag_text)
                            
                            self.scraped_data.append({
                                'page': current_page,
                                'index': i + 1,
                                'quote': quote_text,
                                'author': author_name,
                                'tags': tag_list,
                                'site': 'quotes.toscrape.com'
                            })
                            
                            print(f"  {i+1}. {author_name}: {quote_text[:50]}...")
                            
                        except Exception as e:
                            print(f"명언 {i+1} 처리 중 오류: {e}")
                    
                    # 다음 페이지 확인
                    next_btn = await page.query_selector('.next a')
                    if not next_btn:
                        print("다음 페이지가 없습니다.")
                        break
                    
                    current_page += 1
                    await asyncio.sleep(1)
                    
            finally:
                await browser.close()
    
    async def test_books_site(self):
        """Books to Scrape 사이트 테스트"""
        print("\n=== Books to Scrape 테스트 시작 ===")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            try:
                base_url = "http://books.toscrape.com"
                current_page = 1
                max_pages = 2
                
                while current_page <= max_pages:
                    if current_page == 1:
                        url = base_url
                    else:
                        url = f"{base_url}/catalogue/page-{current_page}.html"
                    
                    print(f"\n페이지 {current_page} 스크래핑: {url}")
                    await page.goto(url)
                    
                    # 책 정보 수집
                    books = await page.query_selector_all('article.product_pod')
                    print(f"발견된 책 수: {len(books)}")
                    
                    for i, book in enumerate(books[:10]):  # 처음 10개만
                        try:
                            title_elem = await book.query_selector('h3 a')
                            price_elem = await book.query_selector('.price_color')
                            rating_elem = await book.query_selector('.star-rating')
                            
                            title = await title_elem.get_attribute('title') if title_elem else ""
                            price = await price_elem.inner_text() if price_elem else ""
                            rating = await rating_elem.get_attribute('class') if rating_elem else ""
                            
                            # 책 상세 페이지 링크
                            book_link = await title_elem.get_attribute('href') if title_elem else ""
                            if book_link:
                                book_url = urljoin(base_url + "/catalogue/", book_link)
                                
                                # 책 상세 정보 가져오기
                                book_detail = await self.get_book_detail(browser, book_url)
                                
                                self.scraped_data.append({
                                    'page': current_page,
                                    'index': i + 1,
                                    'title': title,
                                    'price': price,
                                    'rating': rating,
                                    'url': book_url,
                                    'detail': book_detail,
                                    'site': 'books.toscrape.com'
                                })
                                
                                print(f"  {i+1}. {title} - {price}")
                                
                        except Exception as e:
                            print(f"책 {i+1} 처리 중 오류: {e}")
                    
                    # 다음 페이지 확인
                    next_btn = await page.query_selector('.next a')
                    if not next_btn:
                        print("다음 페이지가 없습니다.")
                        break
                    
                    current_page += 1
                    await asyncio.sleep(1)
                    
            finally:
                await browser.close()
    
    async def get_book_detail(self, browser, book_url):
        """책 상세 정보 가져오기"""
        try:
            detail_page = await browser.new_page()
            await detail_page.goto(book_url)
            
            # 책 설명 가져오기
            description_elem = await detail_page.query_selector('#product_description + p')
            description = await description_elem.inner_text() if description_elem else ""
            
            # 재고 정보
            stock_elem = await detail_page.query_selector('.instock.availability')
            stock = await stock_elem.inner_text() if stock_elem else ""
            
            await detail_page.close()
            
            return {
                'description': description[:200],  # 200자 제한
                'stock': stock.strip()
            }
            
        except Exception as e:
            print(f"상세 정보 가져오기 오류: {e}")
            return {}
    
    async def test_hackernews(self):
        """Hacker News 테스트 (간단한 버전)"""
        print("\n=== Hacker News 테스트 시작 ===")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            try:
                url = "https://news.ycombinator.com/"
                print(f"스크래핑: {url}")
                await page.goto(url)
                
                # 기사 제목들 수집
                articles = await page.query_selector_all('.athing')
                print(f"발견된 기사 수: {len(articles)}")
                
                for i, article in enumerate(articles[:10]):  # 처음 10개만
                    try:
                        title_elem = await article.query_selector('.titleline a')
                        title = await title_elem.inner_text() if title_elem else ""
                        link = await title_elem.get_attribute('href') if title_elem else ""
                        
                        # 점수와 댓글 정보는 다음 형제 요소에 있음
                        article_id = await article.get_attribute('id')
                        
                        self.scraped_data.append({
                            'index': i + 1,
                            'title': title,
                            'link': link,
                            'article_id': article_id,
                            'site': 'news.ycombinator.com'
                        })
                        
                        print(f"  {i+1}. {title[:70]}...")
                        
                    except Exception as e:
                        print(f"기사 {i+1} 처리 중 오류: {e}")
                        
            finally:
                await browser.close()
    
    def save_results(self, filename='test_results.json'):
        """결과 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=2)
        print(f"\n결과가 {filename}에 저장되었습니다.")
    
    def print_summary(self):
        """결과 요약 출력"""
        print(f"\n=== 스크래핑 결과 요약 ===")
        print(f"총 수집된 항목: {len(self.scraped_data)}개")
        
        # 사이트별 통계
        site_stats = {}
        for item in self.scraped_data:
            site = item.get('site', 'unknown')
            site_stats[site] = site_stats.get(site, 0) + 1
        
        for site, count in site_stats.items():
            print(f"  {site}: {count}개")

async def main():
    scraper = TestScraper()
    
    print("웹 스크래핑 테스트를 시작합니다...")
    print("주의: 브라우저 창이 열려서 스크래핑 과정을 볼 수 있습니다.")
    
    # 테스트할 사이트 선택
    test_sites = {
        '1': ('Quotes to Scrape', scraper.test_quotes_site),
        '2': ('Books to Scrape', scraper.test_books_site),
        '3': ('Hacker News', scraper.test_hackernews),
        '4': ('모든 사이트', None)
    }
    
    print("\n테스트할 사이트를 선택하세요:")
    for key, (name, _) in test_sites.items():
        print(f"  {key}. {name}")
    
    choice = input("\n선택 (1-4): ").strip()
    
    if choice == '1':
        await scraper.test_quotes_site()
    elif choice == '2':
        await scraper.test_books_site()
    elif choice == '3':
        await scraper.test_hackernews()
    elif choice == '4':
        await scraper.test_quotes_site()
        await scraper.test_books_site()
        await scraper.test_hackernews()
    else:
        print("잘못된 선택입니다. 기본적으로 Quotes 사이트를 테스트합니다.")
        await scraper.test_quotes_site()
    
    # 결과 출력 및 저장
    scraper.print_summary()
    scraper.save_results()

if __name__ == "__main__":
    asyncio.run(main())
