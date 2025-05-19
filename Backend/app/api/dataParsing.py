from fastapi import FastAPI, HTTPException
from app.schemas.website_crawler import WebsiteData
from app.core.crawler import WebCrawler
from app.db.database import  company_data_collection
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool


app = APIRouter()

@app.post("/crawl")
async def start_crawling(request: WebsiteData):

    base_url = request.base_url
    
    # Instantiate the WebCrawler
    crawler = WebCrawler(base_url=base_url, max_workers=10)
    
    # Run the crawl in threadpool to avoid blocking the event loop
    visited = await run_in_threadpool(crawler.crawl)
    
    print(list(visited),"visited")
    
    if not visited:
        raise HTTPException(status_code=400, detail="No URLs found.")
    
    contents = []
    
    for url in visited:
        print("Inside the loop")
        content = await run_in_threadpool(crawler.fetch_clean_text,url)
        print(url,"response")
        if content:
            contents.append({
                "url":url,
                "content": content
            })
            
    if contents:
        company_data_collection.insert_many(contents)       
        
    return {"message": f"Successfully crawled and saved {len(contents)} pages.", "base_url":base_url} 