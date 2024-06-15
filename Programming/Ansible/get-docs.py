import os
import re
from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin, urlparse

# Set the Ansible documentation URL base
url_base = "https://docs.ansible.com/ansible/latest"

# Create a directory to store the parsed data
data_dir = "ansible_docs_parsed"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def parse_doc(url):
    try:
        # Send an HTTP request and get the HTML response
        response = requests.get(url)
        response.raise_for_status()
        html = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract relevant information from the HTML
        title = soup.find('title').text.strip()
        sections = []
        for h2 in soup.find_all('h2'):
            section_title = h2.text.strip()
            section_links = [a['href'] for a in h2.find_all('a', href=True)]
            sections.append({'title': section_title, 'links': section_links})

        return {'title': title, 'sections': sections}

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None

def write_parsed_data(data, filename):
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(data, f, indent=4)

def crawl_website(url, crawled_urls=set()):
    # Check if the URL is valid and not already crawled
    parsed_url = urlparse(url)
    if '' in (parsed_url.scheme, parsed_url.netloc) or parsed_url.netloc != 'docs.ansible.com':
        return

    if url in crawled_urls:
        print(f"Skipping {url} (already crawled)")
        return

    crawled_urls.add(url)

    # Crawl the webpage and extract data
    data = parse_doc(url)
    if data:
        # Write the parsed data to a JSON file
        filename = os.path.basename(parsed_url.path).replace('.html', '.json')
        if not filename:
            filename = 'index.json'
        write_parsed_data(data, filename)

        # Recursively crawl any linked pages
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        for link in [a['href'] for a in soup.find_all('a', href=True)]:
            full_link = urljoin(url_base, link)
            crawl_website(full_link, crawled_urls)

# Start the crawling process from the root URL
crawl_website(url_base)
