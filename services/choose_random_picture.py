import json
import logging
import random as rd
import os
from services.create_api_connection import create_api_connection
from services.google_cloud_storage import download_blob, list_blobs


base_dir = os.getenv('TMP_DIR', '.')


def choose_random_picture(service, all_pictures):
    """
    Choose a random picture from the pictures folder.

    Args:
        service: The Google Drive service object.
        all_pictures: A list of all pictures in the folder.

    Returns:
        A tuple containing the name of the chosen picture, the month folder
        name, and the year folder name.
    """
    chosen_picture = rd.choice(all_pictures)

    # Get parent folders name of chosen picture on two levels
    month_folder_id = chosen_picture['parents'][0]
    month_folder = service.files().get(fileId=month_folder_id,
                                       fields=("id, kind, name, mimeType, "
                                               "parents")).execute()
    month = month_folder['name']
    # Get parent folder of parent's folder
    year_folder_id = month_folder['parents'][0]
    year_folder = service.files().get(fileId=year_folder_id).execute()
    year = year_folder['name']

    # Downloads chosen picture into tmp_photos folder
    request = service.files().get_media(fileId=chosen_picture['id'])
    if not os.path.exists(f"{base_dir}/tmp_photos"):
        os.mkdir(f"{base_dir}/tmp_photos")
    logging.info(f"Picking picture : {chosen_picture['name']}")
    with open(f"{base_dir}/tmp_photos/{chosen_picture['name']}", "wb") as fh:
        fh.write(request.execute())

    return chosen_picture["name"], month, year


def get_all_pictures(service):
    """
    Retrieves all pictures from a given service.

    Args:
        service: The service object used to interact with the API.

    Returns:
        A list of dictionaries representing the pictures, each containing the
        following keys:
        - id: The ID of the picture file.
        - name: The name of the picture file.
        - mimeType: The MIME type of the picture file.
        - parents: The parent folders of the picture file.
    """
    all_pictures = []
    page_token = None

    while True:
        response = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, parents)",
            q=("mimeType='image/jpeg' or "
               "mimeType='image/png' or"
               "name contains 'HEIC'"),
            pageToken=page_token
        ).execute()

        all_pictures.extend(response['files'])

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return all_pictures


def pictures_to_display():
    """
    Retrieves a list of random pictures and their corresponding month and year,
    and saves the information to a JSON file.

    Returns:
        None
    """
    service = create_api_connection()
    all_pictures = get_all_pictures(service)
    picture_info = []
    for _ in range(int(os.getenv('NUMBER_OF_PICTURES'))):
        picture, month, year = choose_random_picture(service, all_pictures)
        # Appends the info to a json file
        picture_info.append({'picture': picture, 'month': month,
                             'year': year})
    with open(f'{base_dir}/tmp_photos/picture_info.json', 'w') as f:
        json.dump(picture_info, f)


def pictures_to_display_from_blob():
    """
    Downloads pictures from Google Cloud Storage and store them in the
    tmp_photos folder.
    """
    blob_list = list_blobs('pv-cloudstorage')
    logging.info(f'Blob list : {blob_list}')

    for blob in blob_list:
        logging.info(f'Downloading {blob.name}')
        download_blob('pv-cloudstorage', blob.name, 'tmp_photos')
