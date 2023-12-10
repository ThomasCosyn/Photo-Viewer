from services.create_api_connection import create_api_connection


def choose_random_picture():
    """Choose a random picture from the pictures folder."""
    service = create_api_connection()
    years = service.files().list(
        pageSize=2,
        fields="nextPageToken, files(name, mimeType, parents)",
        q="mimeType='application/vnd.google-apps.folder'"
    ).execute()

    return years