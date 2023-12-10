from google.oauth2 import service_account
from googleapiclient.discovery import build


def create_api_connection():
    """
    Creates a connection to the Google Drive API using a service account.

    Returns:
        service (googleapiclient.discovery.Resource): The Google Drive API service object.
    """
    scope = ['https://www.googleapis.com/auth/drive']
    service_account_json_key = './photo-viewer-407717-89d2741837ef.json'
    credentials = service_account.Credentials.from_service_account_file(
        filename=service_account_json_key,
        scopes=scope)
    service = build('drive', 'v3', credentials=credentials)
    return service
