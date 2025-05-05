import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    # 1. SSO 인증된 사용자 프로필 경로 지정
    browser_config = BrowserConfig(
        headless=False,  # 필요시 False로 설정해 동작 확인
        verbose=True,
        use_managed_browser=True,
        browser_type="chromium",
        user_data_dir="D:\temp\chrome-profile"  # 위에서 사용한 경로와 동일하게
    )

    # 2. 크롤링할 페이지 설정 (로그인 필요 페이지)
    crawl_config = CrawlerRunConfig(
        url="https://www.google.com/",
        wait_for="css:.main-content"  # 페이지 로딩 완료 대기용 CSS 선택자
    )

    # 3. 크롤러 실행
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(config=crawl_config)
        if result.success:
            print(result.markdown)  # AI/RAG용 마크다운 추출
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
