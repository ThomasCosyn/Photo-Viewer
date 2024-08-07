import gradio as gr
import json
import logging
import os

from dotenv import load_dotenv
from services.choose_random_picture import pictures_to_display_from_blob
from services.get_secret import get_secret
from services.month_decoder import month_decoder

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

load_dotenv()

base_dir = os.getenv('TMP_DIR', '.')
logging.info(f'Base tmp dir is {base_dir}')

# Delete pictures in tmp_photos
logging.info('Deleting pictures in tmp_photos')
if os.path.exists(f'{base_dir}/tmp_photos'):
    for filename in os.listdir(f'{base_dir}/tmp_photos'):
        os.remove(f'{base_dir}/tmp_photos/{filename}')
    logging.info('Pictures deleted')

# Writes picture to tmp_photos folder
logging.info('Writing random picture to tmp_photos folder')
# pictures_to_display()
pictures_to_display_from_blob()
logging.info('Random picture written to tmp_photos folder')

# Loading pictures metadata to display
picture_info = json.load(open(f'{base_dir}/tmp_photos/picture_info.json'))

# Creates a gradio app that displays the pictures stored in tmp_photos
with gr.Blocks(
    analytics_enabled=False,
    css="footer {visibility: hidden}"
) as iface:
    with gr.Column():
        gr.Markdown("# Mémoire vive\n#### Chaque jour, 12 photos aléatoires \
                    seront affichées. Ce ne seront pas forcément des belles \
                    photos, mais simplement des moments de ma vie dont j'ai \
                    envie de me souvenir et que je souhaite vous partager.")
    with gr.Column():
        for picture in picture_info:
            gr.Markdown(f"## {month_decoder(picture['month'])} "
                        f"{picture['year']}")
            gr.Image(f'{base_dir}/tmp_photos/{picture["picture"]}')

iface.launch(server_name="0.0.0.0",
             server_port=8080,
             auth=(get_secret("username"),
                   get_secret("password")))
