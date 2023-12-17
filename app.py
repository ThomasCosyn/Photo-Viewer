import gradio as gr
import json
import logging
import os
from services.choose_random_picture import pictures_to_display
from services.month_decoder import month_decoder

# TO DO
# Afficher plusieurs photos
# Déployer

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

# Delete pictures in tmp_photos
logging.info('Deleting pictures in tmp_photos')
for filename in os.listdir('tmp_photos'):
    os.remove(f'tmp_photos/{filename}')
logging.info('Pictures deleted')

# Writes picture to tmp_photos folder
logging.info('Writing random picture to tmp_photos folder')
pictures_to_display()
logging.info('Random picture written to tmp_photos folder')

# Loading pictures metadata to display
picture_info = json.load(open('tmp_photos/picture_info.json'))

# Creates a gradio app that displays the pictures stored in tmp_photos
with gr.Blocks() as iface:
    with gr.Row():
        gr.Markdown("# Album photo dynamique")
    with gr.Column():
        gr.Image(f'tmp_photos/{picture_info["picture"]}')
        gr.Markdown(f"## {month_decoder(picture_info['month'])} "
                    f"{picture_info['year']}")

iface.launch()
