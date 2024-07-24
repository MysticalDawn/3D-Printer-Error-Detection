import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import zipfile
import shutil

def download_and_extract_file(url, default_filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Try to get filename from Content-Disposition header
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = content_disposition.split('filename=')[1].strip('"')
    else:
        filename = default_filename
    
    filename = sanitize_filename(filename)
    full_path = os.path.join("downloads", filename)
    
    # If file already exists, add a number to the filename
    counter = 1
    while os.path.exists(full_path):
        name, ext = os.path.splitext(filename)
        full_path = os.path.join("downloads", f"{name}_{counter}{ext}")
        counter += 1
    
    with open(full_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded: {full_path}")

    # Check if the file is a zip and extract it
    if full_path.lower().endswith('.zip'):
        extract_zip(full_path)

def extract_zip(zip_path):
    extract_dir = os.path.splitext(zip_path)[0]  # Remove .zip extension
    temp_dir = extract_dir + "_temp"
    
    # Extract to a temporary directory first
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Move contents to the final directory, avoiding nested folders
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(extract_dir, file)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.move(src_path, dst_path)
    
    # Remove the temporary directory
    shutil.rmtree(temp_dir)
    
    print(f"Extracted: {zip_path} to {extract_dir}")

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
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    page = 1
    while True:
        page_url = f"{item_url}?obo.page={page}"
        print(f"Processing page {page}")
        
        links = get_download_links(page_url)
        if not links:
            break
        
        for link, default_filename in links:
            full_url = f"{base_url}{link}"
            download_and_extract_file(full_url, default_filename)
        
        page += 1

if __name__ == "__main__":
    main()