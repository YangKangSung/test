import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as playwright:
        # Launch the browser in headless mode for production use
        browser = await playwright.chromium.launch(headless=False)  # Set to False for debugging
        page = await browser.new_page()

        try:
            # Navigate to the specified blog URL
            await page.goto('https://www.naver.com/')  # Replace with the actual blog URL

            # Wait for the titles to load
            await page.wait_for_selector('.search_area')

            # Extract blog post titles
            titles = await page.locator('.search_area').all_text_contents()

            # Print the extracted titles
            if titles:
                print("Blog Post Titles:")
                for title in titles:
                    print(title)
            else:
                print("No titles found.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

# Run the asynchronous function
asyncio.run(run())
