from dotenv import load_dotenv
import logging
import os
from services.choose_random_picture import pictures_to_display


load_dotenv()

base_dir = os.getenv('TMP_DIR', '.')
logging.info(f'Base tmp dir is {base_dir}')

# Connects to Google Cloud Storage bucket


# Delete pictures in tmp_photos
logging.info('Deleting pictures in tmp_photos')
if os.path.exists(f'{base_dir}/tmp_photos'):
    for filename in os.listdir(f'{base_dir}/tmp_photos'):
        os.remove(f'{base_dir}/tmp_photos/{filename}')
    logging.info('Pictures deleted')

# Writes picture to tmp_photos folder
logging.info('Writing random picture to tmp_photos folder')
pictures_to_display()
logging.info('Random picture written to tmp_photos folder')
