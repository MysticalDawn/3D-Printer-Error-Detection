from PIL import Image
import os
import io

def fix_and_resave_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                # Open the image using PIL
                with open(input_path, 'rb') as f:
                    image = Image.open(io.BytesIO(f.read()))
                
                # Save the image with a new name, which should fix any corruption
                image.save(output_path, 'JPEG')
                # print(f"Fixed and saved as: {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# Set the input and output directories
directory = '../data/caxton_dataset/'
output_directory = 'caxton_dataset/'

for folder in os.listdir(directory):
    """
    Remaining task: run again for print107, print109
    """
    if (folder.startswith('print')) and (folder not in os.listdir(output_directory)):
        print(f'Processing {folder}...')
        folder_input_path = os.path.join(directory, folder, folder)
        folder_output_path = os.path.join(output_directory, folder)
        # Run the function to fix and resave images for each print folder
        fix_and_resave_images(folder_input_path, folder_output_path)
        print(f'Fixed and saved as: {folder_output_path}')

print("Image fixing process completed. Fixed images are in the 'caxton_dataset_fixed' directory.")

