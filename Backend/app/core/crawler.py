import logging
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import threading

import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebCrawler")


class WebCrawler:
    def __init__(self, base_url, max_workers=10):
        self.base_url = base_url.rstrip('/')
        self.visited = set()
        self.to_visit = set([self.base_url])
        self.lock = threading.Lock()
        self.session = self._init_session()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def _init_session(self):
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            raise_on_status=False
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        session.headers.update({"User-Agent": "Mozilla/5.0"})
        return session
    def crawl(self):
        while self.to_visit:
            current_batch = list(self.to_visit)
            self.to_visit.clear()
            next_to_visit = set()

            futures = [self.executor.submit(self._process_url, url, next_to_visit) for url in current_batch]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"[ERROR] Future task failed: {e}")

            self.to_visit.update(next_to_visit)

        return self.visited

    def _process_url(self, url, next_to_visit):
        with self.lock:
            if url in self.visited:
                return
            self.visited.add(url)

        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Skipped {url}: Status {response.status_code}")
                return

            content_type = response.headers.get("Content-Type", "")
            if "text/html" in content_type:
                soup = BeautifulSoup(response.text, "html.parser")
                for tag in soup.find_all("a", href=True):
                    href = urljoin(url, tag["href"])
                    normalized = self._normalize_url(href)
                    if self._is_valid_url(normalized):
                        with self.lock:
                            if normalized not in self.visited:
                                next_to_visit.add(normalized)

        except Exception as e:
            logger.error(f"[ERROR] Failed to crawl {url}: {e}")

    def fetch_clean_text(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "application/pdf" in content_type or url.lower().endswith(".pdf"):
                return self._parse_pdf(response.content)
            elif "text/html" in content_type:
                return self._parse_html(response.text)
            else:
                logger.warning(f"Unsupported content type at {url}: {content_type}")
                return ""

        except Exception as e:
            logger.error(f"[ERROR] Failed to fetch {url}: {e}")
            return ""

    def _parse_html(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)

    def _parse_pdf(self, pdf_bytes):
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
            return text.strip()
        except Exception as e:
            logger.error(f"[ERROR] PDF parsing failed: {e}")
            return ""

    def _normalize_url(self, url):
        parsed = urlparse(url)
        return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")

    def _is_valid_url(self, url):
        return url.startswith(self.base_url) and url not in self.visited
