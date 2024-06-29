import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from services.get_secret import get_secret


def create_api_connection():
    """
    Creates a connection to the Google Drive API using a service account.

    Returns:
        service (googleapiclient.discovery.Resource): The Google Drive API
        service object.
    """
    scope = ['https://www.googleapis.com/auth/drive']
    service_account_key = get_secret("service-account-key")  # './photo-viewer-407717-89d2741837ef.json'  # noqa
    service_account_info = json.loads(service_account_key)
    credentials = service_account.Credentials.from_service_account_info(
        info=service_account_info,
        scopes=scope
    )
    service = build('drive', 'v3', credentials=credentials)
    return service
