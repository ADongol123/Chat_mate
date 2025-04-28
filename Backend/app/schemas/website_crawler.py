from pydantic import BaseModel

class WebsiteData(BaseModel):
    base_url: str


