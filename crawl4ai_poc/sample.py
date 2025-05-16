# import asyncio
# from crawl4ai import * # type: ignore

# async def main():
#     async with AsyncWebCrawler() as crawler: # type: ignore
#         result = await crawler.arun(
#             url="https://www.nbcnews.com/business",
#         )
#         print(result.markdown)

# if __name__ == "__main__":
#     asyncio.run(main())



import requests

# Submit a crawl job
response = requests.post(
    "http://localhost:11235/crawl",
    json={"urls": "https://example.com", "priority": 10}
)
task_id = response.json()["task_id"]

# Continue polling until the task is complete (status="completed")
result = requests.get(f"http://localhost:11235/task/{task_id}")