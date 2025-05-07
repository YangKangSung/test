import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    chrome_executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    # 1. SSO 인증된 사용자 프로필 경로 지정
    # browser_config = BrowserConfig(
    #     headless=False,  # 필요시 False로 설정해 동작 확인
    #     # executable_path=chrome_executable_path,
    #     verbose=True,
    #     browser_type="chromium",
    #     use_managed_browser=False,      # CDP 사용 등 고급 기능
    #     # use_persistent_context=True,   # ⚠ 반드시 True로 설정
    #     extra_args={
    #         "channel": "chrome",
    #         "executablePath": chrome_executable_path  # Playwright launch()에 전달됨
    #     },
    #     user_data_dir="D:\\temp\\chrome-profile"  # 위에서 사용한 경로와 동일하게
    # )

    browser_config = BrowserConfig(
        browser_type="chromium",           # Playwright 브라우저 유형
        headless=False,
        verbose=True,
        use_persistent_context=True,       # Persistent Context 사용
        user_data_dir="D:\\temp\\chrome-profile",
        playwright_launch_options={
            "channel": "chrome",           # 시스템 Chrome 실행
            "executablePath": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        }
    )

    # 2. 크롤링할 페이지 설정 (로그인 필요 페이지)
    crawl_config = CrawlerRunConfig(
        url="https://www.google.com/",
        wait_for="css:input[name='q']"  # Google search input box selector
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
