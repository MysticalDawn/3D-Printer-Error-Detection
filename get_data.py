import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import zipfile
import shutil
import hashlib
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_extract_file(url, default_filename, expected_md5):
    try:
        response = download_with_retry(url)
        
        filename = get_filename(response, default_filename)
        full_path = get_unique_filepath("caxton_dataset", filename)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192

        with open(full_path, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=block_size):
                size = file.write(chunk)
                progress_bar.update(size)

        print(f"\nDownloaded: {full_path}")

        if verify_file(full_path, expected_md5):
            if full_path.lower().endswith('.zip'):
                extract_zip(full_path)
                os.remove(full_path)
                print(f"Deleted zip file: {full_path}")
        else:
            os.remove(full_path)
            print(f"Deleted corrupted file: {full_path}")
    except Exception as e:
        logging.error(f"Error downloading {url}: {str(e)}", exc_info=True)

def verify_file(file_path, expected_md5):
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        logging.error(f"Downloaded file is empty: {file_path}")
        return False

    if expected_md5 is None:
        logging.warning(f"No MD5 checksum provided for {file_path}. Skipping verification.")
        return True

    if verify_md5(file_path, expected_md5):
        print(f"MD5 checksum verified for {file_path}")
        return True
    else:
        print(f"MD5 checksum verification failed for {file_path}")
        return False

def verify_md5(file_path, expected_md5):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    calculated_md5 = md5_hash.hexdigest()
    print(f"Calculated MD5: {calculated_md5}")
    print(f"Expected MD5:   {expected_md5}")
    return calculated_md5 == expected_md5

def download_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=300)  # 5 minutes timeout
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Download attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise

def get_filename(response, default_filename):
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = content_disposition.split('filename=')[1].strip('"')
    else:
        filename = default_filename
    return sanitize_filename(filename)

def get_unique_filepath(directory, filename):
    full_path = os.path.join(directory, filename)
    counter = 1
    while os.path.exists(full_path):
        name, ext = os.path.splitext(filename)
        full_path = os.path.join(directory, f"{name}_{counter}{ext}")
        counter += 1
    return full_path

def extract_zip(zip_path):
    extract_dir = os.path.splitext(zip_path)[0]
    temp_dir = extract_dir + "_temp"
    
    if os.path.exists(extract_dir):
        print(f"Extraction directory already exists: {extract_dir}")
        return
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(extract_dir, file)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.move(src_path, dst_path)
    
    shutil.rmtree(temp_dir)
    print(f"Extracted: {zip_path} to {extract_dir}")

def get_download_links_and_md5(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = []
    
    for a in soup.find_all('a', class_='dont-break-out'):
        if 'bitstreams' in a['href'] and 'download' in a['href']:
            file_name = a.text.strip()
            parent = a.find_parent('div', class_='file-section')
            if parent:
                md5_span = parent.find('span', class_='md5')
                md5 = md5_span.text.strip() if md5_span else None
                print(f"Found file: {file_name}, MD5: {md5}")  # Add this line for debugging
                download_links.append((a['href'], file_name, md5))
    
    return download_links

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in [' ', '.', '_', '-']]).rstrip()

def main():
    base_url = "https://www.repository.cam.ac.uk"
    item_url = f"{base_url}/items/6d77cd6d-8569-4bf4-9d5f-311ad2a49ac8/full"
    
    if not os.path.exists("caxton_dataset"):
        os.makedirs("caxton_dataset")

    page = 1
    while True:
        page_url = f"{item_url}?obo.page={page}"
        logging.info(f"Processing page {page}")
        links = get_download_links_and_md5(page_url)
        
        if not links:
            logging.info(f"No more links found on page {page}. Stopping.")
            break
        
        for link, default_filename, md5 in links:
            full_url = f"{base_url}{link}"
            logging.info(f"Attempting to download: {full_url}")
            try:
                download_and_extract_file(full_url, default_filename, md5)
            except Exception as e:
                logging.error(f"Failed to process {default_filename}: {e}", exc_info=True)
            
            user_input = input("Continue to next file? (y/n): ")
            if user_input.lower() != 'y':
                return
        
        page += 1

    logging.info("Download process completed")

if __name__ == "__main__":
    main()