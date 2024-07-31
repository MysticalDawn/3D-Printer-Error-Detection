import os
import subprocess
import logging
from datetime import datetime
import concurrent.futures

logging.basicConfig(filename='image_processing.log', level=logging.INFO)

base_directory = 'caxton_dataset/'
mogrify_path = subprocess.run(['which', 'mogrify'], capture_output=True, text=True).stdout.strip()

def process_image(file_path):
    logging.info(f"Processing image: {file_path}")
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return False
    command = [mogrify_path, '-set', 'comment', 'Extraneous bytes removed', file_path]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Successfully processed: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {file_path}: {e}")
        return False

def process_images_in_folder(folder_path):
    logging.info(f"Processing folder: {folder_path}")
    
    # Look for the nested folder with the same name
    nested_folder = os.path.join(folder_path, os.path.basename(folder_path))
    if os.path.isdir(nested_folder):
        folder_path = nested_folder
    
    if not os.path.exists(folder_path):
        logging.error(f"Folder does not exist: {folder_path}")
        return 0
    
    jpg_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
    logging.info(f"Found {len(jpg_files)} .jpg files in {folder_path}")
    
    processed_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_file = {executor.submit(process_image, file_path): file_path for file_path in jpg_files}
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                if future.result():
                    processed_count += 1
            except Exception as exc:
                logging.error(f'{file_path} generated an exception: {exc}')
    
    logging.info(f"Finished processing folder: {folder_path}. Images processed: {processed_count}")
    return processed_count

def process_all_folders():
    start_time = datetime.now()
    total_processed = 0
    
    logging.info(f"Starting processing at: {start_time}")
    logging.info(f"Mogrify path: {mogrify_path}")
    logging.info(f"Current working directory: {os.getcwd()}")
    
    if not os.path.exists(base_directory):
        logging.error(f"Base directory does not exist: {base_directory}")
        return

    folders = [os.path.join(base_directory, folder) for folder in os.listdir(base_directory) if folder.startswith('print') and os.path.isdir(os.path.join(base_directory, folder))]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_folder = {executor.submit(process_images_in_folder, folder): folder for folder in folders}
        for future in concurrent.futures.as_completed(future_to_folder):
            folder = future_to_folder[future]
            try:
                total_processed += future.result()
            except Exception as exc:
                logging.error(f'{folder} generated an exception: {exc}')

    end_time = datetime.now()
    logging.info(f"Total images processed: {total_processed}")
    logging.info(f"Total elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    process_all_folders()