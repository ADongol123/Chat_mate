import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl(url, base_url, visited=None):
    if visited is None:
        visited = set()

    if url in visited:
        return visited
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        print(response.url)
        if response.status_code == 200:
            visited.add(url)  # ✅ Only add if successful
            soup = BeautifulSoup(response.text, "html.parser")

            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                full_url = urljoin(base_url, href)

                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    crawl(full_url, base_url, visited)
        else:
            print(f"Skipping {url}: status code {response.status_code}")
    except Exception as e:
        print(f"Error visiting {url}: {e}")

    return visited


        



def fetch_and_parse(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url,headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script_or_style in soup(['script','style']):
            script_or_style.decompose()
            
        text = soup.get_text(separator=" ",strip=True)
        return text
    except Exception as e:
        print(f"Error fetching {url}:{e}")
        return " "