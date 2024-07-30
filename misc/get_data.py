import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from tqdm import tqdm

def download_file(url, default_filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = content_disposition.split('filename=')[1].strip('"')
    else:
        filename = default_filename
    
    filename = sanitize_filename(filename)
    full_path = os.path.join("downloads", filename)
    
    counter = 1
    while os.path.exists(full_path):
        name, ext = os.path.splitext(filename)
        full_path = os.path.join("downloads", f"{name}_{counter}{ext}")
        counter += 1
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    
    with open(full_path, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(block_size):
            size = file.write(data)
            progress_bar.update(size)
    
    print(f"Downloaded: {full_path}")
    return full_path

def get_download_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = []
    for a in soup.find_all('a', class_='dont-break-out'):
        if 'bitstreams' in a['href'] and 'download' in a['href']:
            file_name = a.text.strip()
            download_links.append((a['href'], file_name))
    return download_links

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in [' ', '.', '_', '-']]).rstrip()

def main():
    base_url = "https://www.repository.cam.ac.uk"
    item_url = f"{base_url}/items/6d77cd6d-8569-4bf4-9d5f-311ad2a49ac8/full"
    
    if not os.path.exists("caxton_dataset"):
        os.makedirs("caxton_dataset")
    
    page = 1
    all_links = []
    
    # First, gather all links
    while True:
        page_url = f"{item_url}?obo.page={page}"
        print(f"Processing page {page}")
        links = get_download_links(page_url)
        if not links:
            break
        all_links.extend(links)
        page += 1
    
    # Now download all files with a progress bar
    for link, default_filename in tqdm(all_links, desc="Overall progress"):
        full_url = f"{base_url}{link}"
        download_file(full_url, default_filename)

if __name__ == "__main__":
    main()