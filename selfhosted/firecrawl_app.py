from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str
    formats: Optional[list] = ["markdown"]
    onlyMainContent: Optional[bool] = True

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/v1/scrape')
def scrape(request: ScrapeRequest, authorization: Optional[str] = Header(None)):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(request.url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Extract main content if requested
        if request.onlyMainContent:
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup
            text = main_content.get_text()
        else:
            text = soup.get_text()
            
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Prepare response data
        response_data = {
            'metadata': {
                'title': soup.title.string if soup.title else '',
                'description': '',
                'sourceURL': request.url,
                'url': request.url,
                'statusCode': response.status_code
            }
        }
        
        # Add description if available
        desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if desc_tag:
            response_data['metadata']['description'] = desc_tag.get('content', '')
        
        # Add requested formats
        if 'markdown' in request.formats:
            response_data['markdown'] = text
        if 'html' in request.formats:
            response_data['html'] = str(soup)
        if 'text' in request.formats:
            response_data['text'] = text
            
        return {
            'success': True,
            'data': response_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3002)