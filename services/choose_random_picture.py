import random as rd
from services.create_api_connection import create_api_connection





def choose_random_picture(all_pictures):
    """Choose a random picture from the pictures folder."""
    service = create_api_connection()
    all_pictures = get_all_pictures(service)

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
    with open(f"tmp_photos/{chosen_picture['name']}", "wb") as fh:
        fh.write(request.execute())

    return chosen_picture["name"], month, year


def get_all_pictures(service):

    all_pictures = []
    page_token = None

    while True:
        response = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, parents)",
            q=("mimeType='image/jpeg' or "
               "mimeType='image/png' or "
               "mimeType='image/heic'"),
            pageToken=page_token
        ).execute()

        all_pictures.extend(response['files'])

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return all_pictures


def pictures_to_display():
    service = create_api_connection()
    all_pictures = get_all_pictures(service)
    for _ in range(10):
        picture, month, year = choose_random_picture(all_pictures)
        # Writes the info to a json file
        with open('tmp_photos/picture_info.json', 'w') as f:
            f.write('{{"picture": "{}", "month": "{}", "year": "{}"}}'
                    .format(picture, month, year))
