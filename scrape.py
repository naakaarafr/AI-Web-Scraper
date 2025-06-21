import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def scrape_website(url):
    """
    Scrape website content using Serper API
    Returns JSON response with extracted content
    """
    print(f"Scraping website: {url}")
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'url': url
    }
    
    try:
        response = requests.post(
            'https://scrape.serper.dev',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print("Successfully scraped content!")
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_content_from_json(json_response):
    """
    Extract relevant content from Serper JSON response
    Returns structured data
    """
    if not json_response:
        return None
    
    extracted_data = {
        'title': json_response.get('title', ''),
        'text': json_response.get('text', ''),
        'links': json_response.get('links', []),
        'images': json_response.get('images', []),
        'meta': {
            'description': json_response.get('meta', {}).get('description', ''),
            'keywords': json_response.get('meta', {}).get('keywords', ''),
            'author': json_response.get('meta', {}).get('author', '')
        },
        'headings': json_response.get('headings', []),
        'url': json_response.get('url', '')
    }
    
    return extracted_data

def clean_text_content(text_content):
    """
    Clean and format text content
    """
    if not text_content:
        return ""
    
    # Remove extra whitespace and empty lines
    cleaned_lines = [line.strip() for line in text_content.split('\n') if line.strip()]
    return '\n'.join(cleaned_lines)

def split_content(content, max_length=6000):
    """
    Split content into chunks if needed
    """
    if isinstance(content, str):
        return [content[i:i + max_length] for i in range(0, len(content), max_length)]
    elif isinstance(content, dict):
        # For JSON content, convert to string first if splitting is needed
        content_str = json.dumps(content, indent=2)
        if len(content_str) > max_length:
            return [content_str[i:i + max_length] for i in range(0, len(content_str), max_length)]
        return [content]
    return [content]

def scrape_and_process(url, return_format='json'):
    """
    Main function to scrape and process website content
    
    Args:
        url (str): Website URL to scrape
        return_format (str): 'json' for structured data, 'text' for clean text only
    
    Returns:
        dict or str: Processed content based on return_format
    """
    # Scrape the website
    raw_data = scrape_website(url)
    
    if not raw_data:
        return None
    
    if return_format == 'json':
        # Return structured JSON data
        processed_data = extract_content_from_json(raw_data)
        return processed_data
    elif return_format == 'text':
        # Return clean text only
        text_content = raw_data.get('text', '')
        return clean_text_content(text_content)
    else:
        # Return raw response
        return raw_data

