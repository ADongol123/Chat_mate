from fastapi import FastAPI, HTTPException
from app.schemas.website_crawler import WebsiteData
from app.core.crawler import crawl,fetch_and_parse
from app.db.database import  company_data_collection
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool


app = APIRouter()

@app.post("/crawl")
async def start_crawling(request: WebsiteData):

    base_url = request.base_url
    
    visited = await run_in_threadpool(crawl,base_url,base_url)
    
    print(list(visited),"visited")
    
    if not visited:
        raise HTTPException(status_code=400, detail="No URLs found.")
    
    contents = []
    
    for url in visited:
        print("Inside the loop")
        content = fetch_and_parse(url)
        print(url,"response")
        if content:
            contents.append({
                "url":url,
                "content": content
            })
            
    if contents:
        company_data_collection.insert_many(contents)       
        
    return {"message": f"Successfully crawled and saved {len(contents)} pages.", "base_url":base_url} 